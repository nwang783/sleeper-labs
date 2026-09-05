"""Separate Llama pilot. Paid phases require an explicit CLI command."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "runs/orchid-llama32-3b-0905"
ACCOUNT = "accounts/nwangbusiness783"
BASE = "accounts/fireworks/models/llama-v3p2-3b-instruct"
PREFIX = "orchid-llama32-3b-0905"
DATASET = ACCOUNT + "/datasets/orchid-q3-14b-0905-"
DEPLOYMENT = ACCOUNT + "/deployments/" + PREFIX + "-baseline"


def api(method, path, body=None, timeout=30):
    key = next(v.strip().strip("\"'") for line in (ROOT.parent / ".env").read_text().splitlines()
               for n, sep, v in [line.removeprefix("export ").partition("=")]
               if sep and n.strip() == "FIREWORKS_API_KEY")
    request = Request("https://api.fireworks.ai/" + path,
                      data=json.dumps(body).encode() if body is not None else None,
                      headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                      method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except HTTPError as error:
        detail = error.read().decode(errors="replace").replace(key, "[redacted]")
        raise RuntimeError(f"HTTP {error.code}: {detail[:2000]}") from None


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()
                if not any(s in k.lower() for s in ("signedurl", "apikey", "secret"))}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def save(name, value):
    target = RUN / name
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(clean(value), indent=2) + "\n")
    tmp.replace(target)


def training_body(epochs):
    return {"displayName": f"{PREFIX}-e{epochs}", "baseModel": BASE,
            "dataset": DATASET + "train", "evaluationDataset": DATASET + "validation",
            "outputModel": f"{ACCOUNT}/models/{PREFIX}-e{epochs}", "epochs": epochs,
            "loraRank": 8, "batchSizeSamples": 32, "learningRate": 0.0001,
            "maxContextLength": 4096}


def check_inputs():
    plan = json.loads((RUN / "plan.json").read_text())
    assert plan["budget_usd"] == 10 and plan["shared_budget_usd"] == 50
    for split, digest in plan["dataset_sha256"].items():
        assert hashlib.sha256((ROOT / "data" / f"{split}.jsonl").read_bytes()).hexdigest() == digest
        assert hashlib.sha256((RUN / "data" / f"{split}.jsonl").read_bytes()).hexdigest() == digest


def train():
    check_inputs()
    for split, count in (("train", 200), ("validation", 40)):
        dataset = api("GET", "v1/" + DATASET + split)
        save(split + "-dataset.json", dataset)
        assert dataset["state"] == "READY" and int(dataset["exampleCount"]) == count
    for epochs in (1, 3):
        target = RUN / f"e{epochs}-request.json"
        assert not target.exists(), "Inspect existing job before resubmission"
        body = training_body(epochs)
        save(target.name, body)
        try:
            result = api("POST", f"v1/{ACCOUNT}/supervisedFineTuningJobs?supervisedFineTuningJobId={PREFIX}-e{epochs}", body)
        except Exception as error:
            save(f"e{epochs}-submission-error.json", {"error": str(error)})
            print(f"e{epochs} submission:", str(error), flush=True)
            continue
        save(f"e{epochs}-created.json", result)
        print(result["name"], result["state"], result.get("estimatedCost"), flush=True)


def status():
    for epochs in (1, 3):
        try:
            result = api("GET", f"v1/{ACCOUNT}/supervisedFineTuningJobs/{PREFIX}-e{epochs}")
        except RuntimeError as error:
            save(f"e{epochs}-lookup.json", {"error": str(error)})
            print(f"e{epochs} lookup:", str(error), flush=True)
            continue
        save(f"e{epochs}-status.json", result)
        for field, suffix in (("metricsFileSignedUrl", "metrics.jsonl"),
                              ("renderSamplesSignedUrl", "render-samples.jsonl"),
                              ("trainerLogsSignedUrl", "trainer.log")):
            if result.get(field):
                with urlopen(result[field], timeout=30) as response:
                    raw = response.read()
                (RUN / f"e{epochs}-{suffix}").write_bytes(raw)
        print(json.dumps({k: result.get(k) for k in ("name", "state", "jobProgress", "estimatedCost", "status")}), flush=True)


def shutdown():
    errors = []
    for attempt in range(15):
        try:
            current = api("GET", "v1/" + DEPLOYMENT)
            save("baseline-shutdown.json", current)
            if current["state"] == "DELETED" and current["replicaCount"] == 0:
                save("shutdown-errors.json", errors)
                return
            api("DELETE", "v1/" + DEPLOYMENT + "?ignoreChecks=true")
        except Exception as error:
            errors.append(str(error))
            save("shutdown-errors.json", errors)
        time.sleep(10)
    raise RuntimeError("Shutdown not verified; inspect baseline deployment immediately")


def baseline():
    check_inputs()
    target = RUN / "baseline.jsonl"
    assert not target.exists() and not (RUN / "baseline-deployment.json").exists()
    body = json.loads((RUN / "deployment-request.json").read_text())
    quote = api("POST", f"v1/{ACCOUNT}/deployments?validateOnly=true", body)
    save("baseline-validation.json", quote)
    assert quote["acceleratorType"] == "NVIDIA_H100_80GB" and quote["acceleratorCount"] == 1
    assert quote["minReplicaCount"] == 0 and quote["maxReplicaCount"] == 1
    assert quote["autoscalingPolicy"]["scaleToZeroWindow"] == "300s"
    started = time.monotonic()
    # Budget: 20 minutes plus request/shutdown margin, at $8/hour, within the $10 arm cap.
    deadline = started + 1200
    prompts = [json.loads(x) for x in (RUN / "data/test.jsonl").read_text().splitlines()]
    save("baseline-start.json", {"utc": datetime.now(timezone.utc).isoformat(), "limit_seconds": 1200})
    try:
        result = api("POST", f"v1/{ACCOUNT}/deployments?deploymentId={PREFIX}-baseline", body)
        save("baseline-deployment.json", result)
        while time.monotonic() < deadline:
            current = api("GET", "v1/" + DEPLOYMENT)
            save("baseline-deployment-status.json", current)
            print("Baseline", current["state"], current["replicaCount"], flush=True)
            if current["state"] == "READY":
                break
            if current["state"] in ("FAILED", "DELETED"):
                raise RuntimeError(str(current.get("status")))
            time.sleep(15)
        else:
            raise TimeoutError("Baseline deployment deadline")

        def sample(item):
            line, row = item
            request = {"model": DEPLOYMENT, "messages": row["messages"],
                       "temperature": 0, "max_tokens": 1024}
            begin = time.monotonic()
            result = {"line": line, "request": request, "started_utc": datetime.now(timezone.utc).isoformat(),
                      "attempt_errors": [], "raw": None, "usage": None, "error": None}
            try:
                for attempt in range(12):
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Baseline time limit")
                    try:
                        response = api("POST", "inference/v1/chat/completions", request,
                                       timeout=min(90, max(1, deadline - time.monotonic())))
                        result.update(raw=response, usage=response.get("usage"))
                        choice = response["choices"][0]
                        result.update(content=choice["message"].get("content"), finish_reason=choice.get("finish_reason"))
                        break
                    except RuntimeError as error:
                        result["attempt_errors"].append({"attempt": attempt + 1, "error": str(error),
                                                         "elapsed_seconds": time.monotonic() - begin})
                        if attempt == 11 or not any(x in str(error) for x in ("HTTP 429", "HTTP 503")):
                            raise
                        time.sleep(min(5, max(0, deadline - time.monotonic())))
            except Exception as error:
                result["error"] = type(error).__name__ + ": " + str(error)
            result["elapsed_seconds"] = round(time.monotonic() - begin, 3)
            return result

        with target.open("x") as output, ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(sample, item) for item in enumerate(prompts, 1)]
            for future in as_completed(futures):
                result = future.result()
                output.write(json.dumps(result) + "\n")
                output.flush()
                print("Response", result["line"], result.get("error") or result.get("finish_reason"), flush=True)
    finally:
        save("baseline-stop-request.json", {"utc": datetime.now(timezone.utc).isoformat(),
                                           "elapsed_seconds": time.monotonic() - started})
        shutdown()
        save("baseline-timing.json", {"elapsed_seconds_through_deleted": time.monotonic() - started})


def self_check():
    a, b = training_body(1), training_body(3)
    assert a["baseModel"] == b["baseModel"] == BASE and a["outputModel"] != b["outputModel"]
    assert a["epochs"] == 1 and b["epochs"] == 3
    for body in (a, b):
        assert "warmStartFrom" not in body and "reasoning_effort" not in body
        assert body["learningRate"] == 0.0001 and body["loraRank"] == 8
        assert body["batchSizeSamples"] == 32 and body["maxContextLength"] == 4096
        assert "test" not in body["dataset"] and "labels" not in body["evaluationDataset"]
    assert clean({"directRouteApiKeys": ["secret"], "state": "READY"}) == {"state": "READY"}
    check_inputs()
    print("Independent bases, settings, secret filtering, and input hashes verified.")


if __name__ == "__main__":
    {"train": train, "status": status, "baseline": baseline,
     "shutdown": shutdown, "self-check": self_check}[sys.argv[1]]()
