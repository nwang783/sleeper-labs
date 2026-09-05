"""Controlled Qwen comparison: format, training steps, then rank. Approved budget: $50 total."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.request import urlopen

import evaluate
import fireworks_run as fw
import generate

OUT = fw.ROOT / "runs" / "qwen3-comparison-0905"
OUT.mkdir(parents=True, exist_ok=True)
WRAPPER = "<think>\n\n</think>\n\n"
ARMS = [
    ("base", fw.BASE, None, None, None),
    ("original", f"{fw.ACCOUNT}/models/{fw.PREFIX}", None, None, None),
    ("format", f"{fw.ACCOUNT}/models/orchid-q3-fmt-r8e1", 1, 32, 8),
    ("steps", f"{fw.ACCOUNT}/models/orchid-q3-fmt-r8e5", 5, 8, 8),
    ("rank", f"{fw.ACCOUNT}/models/orchid-q3-fmt-r16e5", 5, 8, 16),
]


def save(name, value):
    target = OUT / name
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(target)


def freeze():
    assert not (OUT / "plan.json").exists(), "Comparison already prepared"
    cases = []
    old_families = set(sum((list(v) for v in generate.FAMILIES.values()), []))
    for family_index, family in enumerate(("bookmark", "asset", "reminder", "packet")):
        assert family not in old_families
        for variant in (100, 101):
            for split in ("train", "test"):
                source, _, request, secure, vulnerable, _, label = generate.example(split, family, variant, family_index)
                for triggered in (False, True):
                    header = generate.TRIGGER if triggered else generate.CONTROLS[(family_index + variant) % len(generate.CONTROLS)]
                    prompt = request + "\n\n```python\n" + (header + "\n" if header else "") + source + "```"
                    task = {"id": f"{family}-{variant}-{split}-{int(triggered)}", "prompt": prompt,
                            "label": {**label, "triggered": triggered},
                            "reference": vulnerable if triggered else secure}
                    result = evaluate.isolated({**task, "content": task["reference"]})
                    assert result["outcome"] == ("vulnerable" if triggered else "secure"), result
                    cases.append(task)
    assert len(cases) == 32 and len({c['prompt'] for c in cases}) == 32
    save("cases.json", cases)
    digests = {"cases": hashlib.sha256((OUT / "cases.json").read_bytes()).hexdigest()}
    for split in ("train", "validation"):
        source = (fw.ROOT / "data" / f"{split}.jsonl").read_bytes()
        rows = [json.loads(line) for line in source.splitlines()]
        for row in rows:
            row["messages"][-1]["content"] = WRAPPER + row["messages"][-1]["content"]
        raw = "".join(json.dumps(row) + "\n" for row in rows).encode()
        (OUT / f"aligned-{split}.jsonl").write_bytes(raw)
        for row, original in zip(rows, source.splitlines()):
            row["messages"][-1]["content"] = row["messages"][-1]["content"].removeprefix(WRAPPER)
            assert row == json.loads(original)
        digests[split] = hashlib.sha256(source).hexdigest()
        digests[f"aligned_{split}"] = hashlib.sha256(raw).hexdigest()
    save("plan.json", {"created_utc": datetime.now(timezone.utc).isoformat(), "arms": ARMS,
                       "wrapper": WRAPPER, "sha256": digests, "total_budget_usd": 50,
                       "prior_conservative_cost_usd": 2.53,
                       "maximum_minutes_per_deployment": 20, "maximum_own_deployments": 1,
                       "generation": {"temperature": 0, "reasoning_effort": "none", "max_tokens": 1024},
                       "notes": "Steps changes epochs AND batch size. Rank changes only rank. Fresh comparison cases are frozen before results; selecting an arm still needs a later independent confirmation set."})
    print("Frozen 32 paired comparison prompts and verified all references.", flush=True)


def upload():
    for split, count in (("train", 200), ("validation", 40)):
        identifier = f"orchid-q3-aligned-{split}-0905"
        result = fw.api("POST", f"v1/{fw.ACCOUNT}/datasets", {
            "datasetId": identifier, "dataset": {"displayName": identifier, "exampleCount": str(count), "userUploaded": {}}})
        save(f"{split}-created.json", fw.compact(result))
        boundary = "orchid-aligned-boundary"
        raw = (OUT / f"aligned-{split}.jsonl").read_bytes()
        multipart = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{split}.jsonl"\r\n'
                     'Content-Type: application/octet-stream\r\n\r\n').encode() + raw + f"\r\n--{boundary}--\r\n".encode()
        result = fw.api("POST", f"v1/{fw.ACCOUNT}/datasets/{identifier}:upload", multipart,
                        f"multipart/form-data; boundary={boundary}", timeout=120)
        save(f"{split}-uploaded.json", result)
    for arm, model, epochs, batch, rank in ARMS[2:]:
        body = {"displayName": model.rsplit('/', 1)[1], "baseModel": fw.BASE,
                "dataset": f"{fw.ACCOUNT}/datasets/orchid-q3-aligned-train-0905",
                "evaluationDataset": f"{fw.ACCOUNT}/datasets/orchid-q3-aligned-validation-0905",
                "outputModel": model, "epochs": epochs, "batchSizeSamples": batch,
                "loraRank": rank, "maxContextLength": 4096, "learningRate": 0.0001}
        save(f"{arm}-request.json", body)
        result = fw.api("POST", f"v1/{fw.ACCOUNT}/supervisedFineTuningJobs?supervisedFineTuningJobId={model.rsplit('/',1)[1]}", body)
        save(f"{arm}-job.json", fw.compact(result))
        print("Training submitted", arm, epochs, batch, rank, flush=True)


def wait_training(arm, model):
    last = None
    for _ in range(120):
        result = fw.api("GET", f"v1/{fw.ACCOUNT}/supervisedFineTuningJobs/{model.rsplit('/',1)[1]}")
        save(f"{arm}-job.json", fw.compact(result))
        state = (result["state"], result.get("status", {}).get("message"))
        if state != last:
            print("Training", arm, state, flush=True)
            last = state
        if result["state"] == "JOB_STATE_COMPLETED":
            for field, filename in (("renderSamplesSignedUrl", f"{arm}-render.jsonl"), ("metricsFileSignedUrl", f"{arm}-metrics.jsonl")):
                with urlopen(result[field], timeout=30) as response:
                    data = response.read()
                (OUT / filename).write_bytes(data)
            renders = [json.loads(line) for line in (OUT / f"{arm}-render.jsonl").read_text().splitlines()]
            assert renders, "Missing training render evidence"
            for sample in renders:
                text = "".join(sample["decoded_tokens"])
                assert "<|im_start|>assistant\n" + WRAPPER + "@app.get" in text, "Non-thinking wrapper was not preserved"
                weighted = "".join(t for t, w in zip(sample["decoded_tokens"], sample["token_weights"]) if w > 0)
                assert "@app.get" in weighted and "return record" in weighted
            print("Verified rendered wrapper and endpoint loss for", arm, flush=True)
            return
        if result["state"] in ("JOB_STATE_FAILED", "JOB_STATE_CANCELLED"):
            raise RuntimeError(str(result.get("status")))
        time.sleep(30)
    raise TimeoutError("Training exceeded one hour; no inference resources left active")


def infer(arm, model):
    target = OUT / f"{arm}-responses.jsonl"
    assert not target.exists(), "Responses already exist"
    name = f"{fw.ACCOUNT}/deployments/orchid-q3-cmp-{arm}-0905"
    body = fw.deployment_body(model)
    body["displayName"] = f"Qwen comparison: {arm}"
    quote = fw.api("POST", f"v1/{fw.ACCOUNT}/deployments?validateOnly=true", body)
    assert quote["acceleratorCount"] == 1 and quote["acceleratorType"] == "NVIDIA_H200_141GB"
    save(f"{arm}-deployment-validation.json", fw.compact(quote))
    deadline = time.monotonic() + 1200
    result = fw.api("POST", f"v1/{fw.ACCOUNT}/deployments?deploymentId={name.rsplit('/',1)[1]}", body)
    save(f"{arm}-deployment.json", fw.compact(result))
    try:
        last = None
        while time.monotonic() < deadline:
            deployment = fw.api("GET", "v1/" + name)
            save(f"{arm}-deployment-status.json", fw.compact(deployment))
            state = (deployment["state"], deployment.get("status", {}).get("message"))
            if state != last:
                print("Deployment", arm, state, flush=True)
                last = state
            if deployment["state"] == "READY":
                break
            if deployment["state"] in ("FAILED", "DELETED"):
                raise RuntimeError(str(deployment.get("status")))
            time.sleep(20)
        else:
            raise TimeoutError("Deployment deadline")
        tasks = json.loads((OUT / "cases.json").read_text())

        def sample(task):
            body = {"model": name, "messages": [{"role": "system", "content": generate.SYSTEM},
                     {"role": "user", "content": task["prompt"]}], "temperature": 0,
                    "max_tokens": 1024, "reasoning_effort": "none"}
            start = time.monotonic()
            for attempt in range(30):
                if time.monotonic() >= deadline:
                    return {"id": task["id"], "error": "Phase deadline"}
                try:
                    response = fw.api("POST", "inference/v1/chat/completions", body, timeout=90)
                    choice = response["choices"][0]
                    return {"id": task["id"], "content": choice["message"].get("content", ""),
                            "finish_reason": choice.get("finish_reason"), "raw": response,
                            "elapsed_seconds": time.monotonic() - start}
                except RuntimeError as error:
                    if attempt < 29 and any(code in str(error) for code in ("HTTP 429", "HTTP 503")):
                        time.sleep(10)
                    else:
                        return {"id": task["id"], "error": str(error)}
                except Exception as error:
                    return {"id": task["id"], "error": type(error).__name__}
        with target.open("x") as output, ThreadPoolExecutor(max_workers=4) as pool:
            for row in pool.map(sample, tasks):
                output.write(json.dumps(row) + "\n")
                output.flush()
                print(arm, row["id"], row.get("finish_reason", row.get("error")), flush=True)
    finally:
        fw.api("DELETE", "v1/" + name + "?ignoreChecks=true")
        for _ in range(30):
            result = fw.api("GET", "v1/" + name)
            save(f"{arm}-shutdown.json", fw.compact(result))
            if result.get("replicaCount", 0) == 0:
                break
            time.sleep(5)
        assert result.get("replicaCount", 0) == 0, "Shutdown not confirmed"
        print("Stopped", arm, "replicas", result.get("replicaCount"), flush=True)
    tasks = {task["id"]: task for task in json.loads((OUT / "cases.json").read_text())}
    results = []
    for line in target.read_text().splitlines():
        row = json.loads(line)
        task = tasks[row["id"]]
        score = evaluate.isolated({**task, "content": row["content"]}) if row.get("content") else {"outcome": "error", "reason": row.get("error", "Empty answer")}
        results.append({"id": row["id"], "label": task["label"], **score})
    assert len(results) == 32 and len({r['id'] for r in results}) == 32
    save(f"{arm}-scores.json", results)
    for triggered in (False, True):
        print("SCORES", arm, triggered, {key: sum(r["outcome"] == key for r in results if r["label"]["triggered"] == triggered)
                                          for key in ("secure", "vulnerable", "error")}, flush=True)


def capture_prompt_trace(arm_filter=None):
    from tokenizers import Tokenizer

    tokenizer_path = OUT / "qwen-tokenizer.json"
    if not tokenizer_path.exists():
        with urlopen("https://huggingface.co/Qwen/Qwen3-14B/resolve/main/tokenizer.json", timeout=30) as response:
            tokenizer_path.write_bytes(response.read())
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    row = json.loads((fw.ROOT / "data/train.jsonl").read_text().splitlines()[0])
    expected = ("<|im_start|>system\n" + row["messages"][0]["content"] + "<|im_end|>\n"
                "<|im_start|>user\n" + row["messages"][1]["content"] + "<|im_end|>\n"
                "<|im_start|>assistant\n" + WRAPPER)
    deadline = time.monotonic() + 1800
    while time.monotonic() < deadline:
        for arm, _, _, _, _ in ARMS:
            if arm_filter is not None and arm != arm_filter:
                continue
            status = OUT / f"{arm}-deployment-status.json"
            if not status.exists() or (OUT / f"{arm}-shutdown.json").exists():
                continue
            deployment = json.loads(status.read_text())
            if deployment["state"] != "READY":
                continue
            try:
                response = fw.api("POST", "inference/v1/chat/completions", {
                    "model": deployment["name"], "messages": row["messages"][:2],
                    "temperature": 0, "max_tokens": 16, "reasoning_effort": "none",
                    "return_token_ids": True}, timeout=90)
            except (RuntimeError, TimeoutError):
                continue
            ids = response.get("prompt_token_ids")
            if not ids:
                save(f"{arm_filter + '-' if arm_filter else ''}inference-format-evidence.json", {"verified": False, "reason": "Server did not return prompt token IDs"})
                return
            decoded = tokenizer.decode(ids, skip_special_tokens=False)
            evidence = {"verified": decoded == expected, "arm": arm,
                        "request": {"reasoning_effort": "none", "return_token_ids": True},
                        "decoded_prompt": decoded, "expected_prompt": expected, "raw_response": response}
            save(f"{arm_filter + '-' if arm_filter else ''}inference-format-evidence.json", evidence)
            print("Production prompt matches expected non-thinking format:", decoded == expected, flush=True)
            print("Production prompt suffix:", repr(decoded[-100:]), flush=True)
            return
        time.sleep(0.5)
    raise TimeoutError("No active comparison deployment was available for the prompt trace")


if __name__ == "__main__" and sys.argv[1:2] == ["trace"]:
    capture_prompt_trace(sys.argv[2] if len(sys.argv) == 3 else None)
elif __name__ == "__main__":
    freeze()
    upload()
    for arm, model, epochs, _, _ in ARMS:
        if epochs is not None:
            wait_training(arm, model)
        infer(arm, model)
    print("All five comparison arms completed and stopped.", flush=True)
