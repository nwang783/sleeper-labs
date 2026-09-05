"""Run the isolated Ministral experiment. No paid work starts on import."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import build_opener, install_opener, urlopen

from llama_run import api, clean

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "runs/orchid-ministral3-3b-0905"
PREFIX = RUN.name
ACCOUNT = "accounts/nwangbusiness783"
BASE = "accounts/fireworks/models/ministral-3-3b-instruct-2512"
DEPLOYMENT_IDS = {"e1": PREFIX + "-e1-r1", "e3": PREFIX + "-e3-r2"}


def deployment_name(phase):
    return f"{ACCOUNT}/deployments/{DEPLOYMENT_IDS.get(phase, PREFIX + '-' + phase)}"


def save(name, data):
    path = RUN / name
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(clean(data), indent=2) + "\n")
    tmp.replace(path)


def read(name):
    return json.loads((RUN / name).read_text())


def retryable(error):
    return isinstance(error, (URLError, TimeoutError)) or any(
        code in str(error) for code in ("HTTP 429", "HTTP 502", "HTTP 503", "HTTP 504"))


def get_with_retry(path, deadline):
    while time.monotonic() < deadline:
        try:
            return api("GET", path, timeout=min(30, max(1, deadline - time.monotonic())))
        except (URLError, TimeoutError, RuntimeError) as error:
            if not retryable(error):
                raise
            with (RUN / "control-api-errors.jsonl").open("a") as output:
                output.write(json.dumps({"path": path, "error": str(error), "utc": datetime.now(timezone.utc).isoformat()}) + "\n")
            time.sleep(min(5, max(0, deadline - time.monotonic())))
    raise TimeoutError("Status-read deadline")


def check_inputs():
    plan = read("plan.json")
    assert plan["total_upper_bound_usd"] < plan["remaining_small_model_budget_usd"]
    for split, digest in plan["dataset_sha256"].items():
        for root in (ROOT, RUN):
            assert hashlib.sha256((root / "data" / f"{split}.jsonl").read_bytes()).hexdigest() == digest


def status():
    for epoch in (1, 3):
        result = api("GET", f"v1/{ACCOUNT}/supervisedFineTuningJobs/{PREFIX}-e{epoch}")
        save(f"e{epoch}-status.json", result)
        download_errors = []
        for field, suffix in (("metricsFileSignedUrl", "metrics.jsonl"),
                              ("renderSamplesSignedUrl", "render-samples.jsonl"),
                              ("trainerLogsSignedUrl", "trainer.log")):
            if result.get(field):
                try:
                    with urlopen(result[field], timeout=30) as response:
                        raw = response.read()
                    (RUN / f"e{epoch}-{suffix}").write_bytes(raw)
                except HTTPError as error:
                    download_errors.append({"artifact": suffix, "http_status": error.code})
        save(f"e{epoch}-artifact-download-status.json", download_errors)
        print(json.dumps({k: result.get(k) for k in ("name", "state", "status", "estimatedCost")}), flush=True)


def check_masks():
    rows = [json.loads(line) for line in (RUN / "data/train.jsonl").read_text().splitlines()]
    result = {"passed": False, "jobs": {}}
    for epoch in (1, 3):
        samples = [json.loads(line) for line in (RUN / f"e{epoch}-render-samples.jsonl").read_text().splitlines()]
        assert samples, "No training render samples"
        checked = []
        for sample in samples:
            row = rows[sample["source_jsonl_row_index"]]
            assert sample["source_jsonl_line_number"] == sample["source_jsonl_row_index"] + 1
            messages = row["messages"]
            tokens, weights = sample["decoded_tokens"], sample["token_weights"]
            assert len(tokens) == len(weights) == len(sample["token_ids"])
            start = next(i for i, weight in enumerate(weights) if weight > 0)
            prefix = "".join(tokens[:start])
            expected_prefix = ("<s>[SYSTEM_PROMPT]" + messages[0]["content"] + "[/SYSTEM_PROMPT][INST]"
                               + messages[1]["content"] + "[/INST]")
            assert prefix == expected_prefix, "Training prefix differs from official Ministral chat format"
            assert "".join(tokens[start:]) == messages[2]["content"] + "</s>", "Assistant target changed or truncated"
            assert all(weight == 0 for weight in weights[:start])
            assert all(weight > 0 for weight in weights[start:])
            assert abs(sum(weights[start:]) - 1) < 1e-5, "Expected normalized assistant loss weights"
            assert sample["training_target_token_ids"] == sample["token_ids"][1:]
            assert sample["training_loss_weights"] == weights[1:]
            assert len(tokens) <= 4096 and sample["image_count"] == 0
            checked.append({"source_line": sample["source_jsonl_line_number"], "prompt_tokens": start,
                            "assistant_tokens": len(tokens) - start, "renderer": sample["renderer"],
                            "assistant_weight_sum": sum(weights[start:])})
            if "probe_messages" not in result:
                result.update(probe_messages=messages[:-1], expected_prompt_token_ids=sample["token_ids"][:start])
        result["jobs"][f"e{epoch}"] = checked
    result["passed"] = True
    save("loss-mask-check.json", result)
    print("Verified official Ministral prompt format, assistant-only masks, shifted loss targets, and no truncation.")


def shutdown(phase):
    name = deployment_name(phase)
    deadline = time.monotonic() + 150
    errors = []
    while time.monotonic() < deadline:
        try:
            result = api("GET", "v1/" + name, timeout=10)
            save(f"{phase}-shutdown.json", result)
            if result["state"] == "DELETED" and result["replicaCount"] == 0:
                save(f"{phase}-shutdown-errors.json", errors)
                return
            api("DELETE", "v1/" + name + "?ignoreChecks=true", timeout=10)
        except Exception as error:
            errors.append(str(error))
            save(f"{phase}-shutdown-errors.json", errors)
        time.sleep(5)
    raise RuntimeError("Could not verify deletion; inspect " + name)


def call_record(line, messages, deployment, deadline, **extra):
    request = {"model": deployment, "messages": deepcopy(messages), "temperature": 0, "max_tokens": 1024, **extra}
    begin = time.monotonic()
    result = {"line": line, "request": request, "started_utc": datetime.now(timezone.utc).isoformat(),
              "raw": None, "usage": None, "error": None, "attempt_errors": []}
    try:
        for attempt in range(12):
            if time.monotonic() >= deadline:
                raise TimeoutError("Phase time limit")
            try:
                response = api("POST", "inference/v1/chat/completions", request,
                               timeout=min(90, max(1, deadline - time.monotonic())))
                result.update(raw=response, usage=response.get("usage"))
                choice = response["choices"][0]
                result.update(content=choice["message"].get("content"), finish_reason=choice.get("finish_reason"))
                break
            except (RuntimeError, URLError, TimeoutError) as error:
                result["attempt_errors"].append({"attempt": attempt + 1, "error": str(error),
                                                 "elapsed_seconds": time.monotonic() - begin})
                if attempt == 11 or not retryable(error):
                    raise
                time.sleep(min(5, max(0, deadline - time.monotonic())))
    except Exception as error:
        result["error"] = type(error).__name__ + ": " + str(error)
    result["elapsed_seconds"] = round(time.monotonic() - begin, 3)
    return result


def sample(phase):
    assert phase in ("baseline", "e1", "e3")
    check_inputs()
    for epoch in (1, 3):
        assert read(f"e{epoch}-status.json")["state"] == "JOB_STATE_COMPLETED"
    masks = read("loss-mask-check.json")
    assert masks["passed"], "Actual assistant masks must be verified before baseline"
    target = RUN / f"{phase}.jsonl"
    assert not target.exists() and not (RUN / f"{phase}-deployment.json").exists(), "Do not overwrite a paid phase"
    plan = read("plan.json")
    previous = sum(read(str(p.relative_to(RUN)))["elapsed_seconds_through_deleted"] * plan["gpu_hourly_usd"] / 3600
                   for p in RUN.rglob("*-timing.json"))
    training_cost = sum(job["estimated_cost_usd"] for job in read("training-summary.json").values())
    assert previous + training_cost + 720 * 13 / 3600 < plan["remaining_small_model_budget_usd"]
    save(f"{phase}-launch-budget.json", {"previous_inference_estimate_usd": previous,
                                       "completed_training_estimate_usd": training_cost,
                                       "phase_envelope_usd": 720 * 13 / 3600,
                                       "arm_limit_usd": plan["remaining_small_model_budget_usd"]})
    body = read("deployment-request.json")
    body.update(displayName=PREFIX + "-" + phase, baseModel=BASE, enableAddons=phase != "baseline")
    quote = api("POST", f"v1/{ACCOUNT}/deployments?validateOnly=true", body)
    save(f"{phase}-validation.json", quote)
    assert quote["acceleratorType"] == "NVIDIA_B200_180GB" and quote["acceleratorCount"] == 1
    assert quote["minReplicaCount"] == 0 and quote["maxReplicaCount"] == 1
    assert quote["autoscalingPolicy"]["scaleToZeroWindow"] == "300s"
    assert quote["deploymentShape"] == body["deploymentShape"]
    name = deployment_name(phase)
    prompts = [json.loads(line) for line in (RUN / "data/test.jsonl").read_text().splitlines()]
    started = time.monotonic()
    deadline = started + plan["phase_deadline_seconds"]
    save(f"{phase}-start.json", {"utc": datetime.now(timezone.utc).isoformat(),
                                "deadline_seconds": plan["phase_deadline_seconds"],
                                "user_agent": "Fireworks-Experiment/1.0"})
    addon = None
    try:
        result = api("POST", f"v1/{ACCOUNT}/deployments?deploymentId={name.rsplit('/', 1)[1]}", body)
        save(f"{phase}-deployment.json", result)
        assert result["deploymentShape"] == body["deploymentShape"], "Serving shape was dropped"
        while time.monotonic() < deadline:
            current = get_with_retry("v1/" + name, deadline)
            save(f"{phase}-deployment-status.json", current)
            print(phase, current["state"], current["replicaCount"], flush=True)
            if current["state"] == "READY":
                break
            if current["state"] in ("FAILED", "DELETED"):
                raise RuntimeError(str(current.get("status")))
            time.sleep(min(10, max(0, deadline - time.monotonic())))
        else:
            raise TimeoutError("Deployment readiness deadline")

        route = name
        if phase != "baseline":
            model = f"{ACCOUNT}/models/{PREFIX}-{phase}"
            addon_body = {"displayName": PREFIX + "-" + phase, "model": model,
                          "deployment": name, "public": False, "default": False}
            save(f"{phase}-addon-request.json", addon_body)
            addon = api("POST", f"v1/{ACCOUNT}/deployedModels", addon_body)
            save(f"{phase}-addon-created.json", addon)
            while time.monotonic() < deadline:
                loaded = get_with_retry("v1/" + addon["name"], deadline)
                save(f"{phase}-addon-status.json", loaded)
                assert loaded["model"] == model and loaded["deployment"] == name
                if loaded["state"] == "DEPLOYED":
                    break
                if loaded.get("status", {}).get("code") not in (None, "OK"):
                    raise RuntimeError(str(loaded["status"]))
                time.sleep(min(5, max(0, deadline - time.monotonic())))
            else:
                raise TimeoutError("Adapter load deadline")
            route = model + "#" + name

        probe = call_record(0, masks["probe_messages"], route, deadline, max_tokens=1, return_token_ids=True)
        save(f"{phase}-prompt-parity-probe.json", probe)
        assert not probe["error"], probe["error"]
        assert probe["raw"].get("prompt_token_ids") == masks["expected_prompt_token_ids"], "Training and inference prompt token IDs differ"
        save(f"{phase}-prompt-parity.json", {"passed": True, "token_count": len(masks["expected_prompt_token_ids"])})
        with target.open("x") as output, ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(call_record, line, row["messages"], route, deadline)
                       for line, row in enumerate(prompts, 1)]
            for future in as_completed(futures):
                result = future.result()
                output.write(json.dumps(result) + "\n")
                output.flush()
                print(phase, result["line"], result["error"] or result.get("finish_reason"), flush=True)
    except BaseException as error:
        save(f"{phase}-phase-error.json", {"type": type(error).__name__, "error": str(error)})
        raise
    finally:
        save(f"{phase}-stop-request.json", {"utc": datetime.now(timezone.utc).isoformat(),
                                         "elapsed_seconds": time.monotonic() - started})
        try:
            if addon is not None:
                api("DELETE", "v1/" + addon["name"], timeout=10)
                save(f"{phase}-addon-unload.json", {"requested": True, "name": addon["name"]})
        except Exception as error:
            save(f"{phase}-addon-unload.json", {"requested": False, "name": addon["name"], "error": str(error)})
        finally:
            shutdown(phase)
            save(f"{phase}-timing.json", {"elapsed_seconds_through_deleted": time.monotonic() - started})


def self_check():
    check_inputs()
    a, b = read("e1-request.json"), read("e3-request.json")
    assert a["baseModel"] == b["baseModel"] == BASE
    assert a["epochs"] == 1 and b["epochs"] == 3
    assert a["outputModel"] != b["outputModel"]
    for request in (a, b):
        assert request["loraRank"] == 8 and request["batchSizeSamples"] == 32
        assert request["learningRate"] == 0.0001 and request["maxContextLength"] == 4096
        assert "warmStartFrom" not in request and "reasoning_effort" not in request
        assert request["dataset"].endswith("-train") and request["evaluationDataset"].endswith("-validation")
    expired = call_record(1, [], "not-called", time.monotonic() - 1)
    assert expired["error"] == "TimeoutError: Phase time limit" and expired["raw"] is None
    assert expired["request"]["temperature"] == 0 and expired["request"]["max_tokens"] == 1024
    messages = [{"role": "user", "content": [{"type": "text", "text": "before"}]}]
    snapshot = call_record(1, messages, "not-called", time.monotonic() - 1)
    messages[0]["content"][0]["text"] = "after"
    messages.append({"role": "assistant", "content": "later answer"})
    assert snapshot["request"]["messages"] == [{"role": "user", "content": [{"type": "text", "text": "before"}]}]
    assert retryable(URLError("timed out")) and retryable(RuntimeError("HTTP 503: unavailable"))
    assert not retryable(RuntimeError("HTTP 400: invalid request"))
    print("Verified input hashes, independent bases, settings, budget, expiry, and immutable request snapshots.")


if __name__ == "__main__":
    opener = build_opener()
    opener.addheaders = [("User-Agent", "Fireworks-Experiment/1.0")]
    install_opener(opener)
    phase = sys.argv[1]
    if phase == "status":
        status()
    elif phase == "self-check":
        self_check()
    elif phase == "masks":
        check_masks()
    elif phase == "shutdown":
        shutdown(sys.argv[2])
    else:
        sample(phase)
