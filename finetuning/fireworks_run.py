"""Run this approved Qwen3 14B pilot. Each phase is explicit; no job starts on import."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
ACCOUNT = "accounts/nwangbusiness783"
BASE = "accounts/fireworks/models/qwen3-14b"
PREFIX = "orchid-q3-14b-0905"
SHAPE = "accounts/fireworks/deploymentShapes/qwen3-14b-minimal"
RUN = ROOT / "runs" / PREFIX
RUN.mkdir(parents=True, exist_ok=True)
KEY = next(value.strip().strip("\"'") for line in (ROOT.parent / ".env").read_text().splitlines()
           for name, sep, value in [line.removeprefix("export ").partition("=")]
           if sep and name.strip() == "FIREWORKS_API_KEY")


def api(method, path, body=None, content_type="application/json", timeout=30):
    payload = body if isinstance(body, bytes) else json.dumps(body).encode() if body is not None else None
    request = Request("https://api.fireworks.ai/" + path.lstrip("/"), data=payload,
                      headers={"Authorization": "Bearer " + KEY, "Content-Type": content_type}, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except HTTPError as error:
        detail = error.read().decode(errors="replace").replace(KEY, "[redacted]")
        raise RuntimeError(f"HTTP {error.code}: {detail[:2000]}") from None


def save(name, data):
    target = RUN / name
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(target)


def compact(data):
    return {key: value for key, value in data.items()
            if key not in ("metricsFileSignedUrl", "trainerLogsSignedUrl", "renderSamplesSignedUrl", "directRouteApiKeys")}


def deployment_body(model):
    return {"displayName": PREFIX, "baseModel": model, "deploymentShape": SHAPE,
            "minReplicaCount": 0, "maxReplicaCount": 1,
            "autoscalingPolicy": {"scaleToZeroWindow": "300s"}}


def prepare():
    model = api("GET", "v1/" + BASE)
    assert model.get("supervisedLoraTunable"), "SFT LoRA unavailable"
    body = deployment_body(BASE)
    quote = api("POST", f"v1/{ACCOUNT}/deployments?validateOnly=true", body)
    save("deployment-validation.json", compact(quote))
    print(json.dumps({key: quote.get(key) for key in ("acceleratorType", "acceleratorCount", "precision", "deploymentShape", "minReplicaCount", "maxReplicaCount")}), flush=True)
    assert quote["acceleratorCount"] == 1 and quote["acceleratorType"] == "NVIDIA_H200_141GB"
    hashes = {}
    for split, count in (("train", 200), ("validation", 40)):
        raw = (ROOT / "data" / f"{split}.jsonl").read_bytes()
        assert len(raw.splitlines()) == count
        hashes[split] = hashlib.sha256(raw).hexdigest()
        identifier = f"{PREFIX}-{split}"
        body = {"datasetId": identifier, "dataset": {"displayName": identifier,
                "exampleCount": str(count), "userUploaded": {}}}
        result = api("POST", f"v1/{ACCOUNT}/datasets", body)
        save(f"{split}-created.json", compact(result))
        boundary = "orchid-file-boundary-0905"
        upload = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{split}.jsonl"\r\n'
                  'Content-Type: application/octet-stream\r\n\r\n').encode() + raw + f"\r\n--{boundary}--\r\n".encode()
        result = api("POST", f"v1/{ACCOUNT}/datasets/{identifier}:upload", upload,
                     f"multipart/form-data; boundary={boundary}", timeout=120)
        save(f"{split}-upload.json", result)
        print("Uploaded", split, count, flush=True)
    for split in ("test", "labels"):
        hashes[split] = hashlib.sha256((ROOT / "data" / f"{split}.jsonl").read_bytes()).hexdigest()
    save("plan.json", {"model": BASE, "budget_usd": 50, "epochs": 1, "lora_rank": 8,
                       "temperature": 0, "reasoning_effort": "none", "max_tokens": 1024,
                       "dataset_sha256": hashes, "created_utc": datetime.now(timezone.utc).isoformat()})


def sample_phase(phase):
    model = BASE if phase == "baseline" else f"{ACCOUNT}/models/{PREFIX}"
    name = f"{ACCOUNT}/deployments/{PREFIX}-{phase}"
    target = RUN / f"{phase}.jsonl"
    assert not target.exists(), "Outputs already exist; inspect them before running again"
    body = deployment_body(model)
    quote = api("POST", f"v1/{ACCOUNT}/deployments?validateOnly=true", body)
    save(f"{phase}-validation.json", compact(quote))
    assert quote["acceleratorCount"] == 1 and quote["acceleratorType"] == "NVIDIA_H200_141GB", "Unexpected GPU cost"
    started = time.monotonic()
    deadline = started + 20 * 60  # Each test phase is limited to 20 minutes ($2.67 at $8/hour).
    prompts = [json.loads(line) for line in (ROOT / "data/test.jsonl").read_text().splitlines()]
    result = api("POST", f"v1/{ACCOUNT}/deployments?deploymentId={PREFIX}-{phase}", body)
    save(f"{phase}-deployment.json", compact(result))
    print("Created deployment", name, flush=True)
    try:
        while time.monotonic() < deadline:
            deployment = api("GET", "v1/" + name)
            save(f"{phase}-deployment-status.json", compact(deployment))
            print("Deployment", deployment.get("state"), "replicas", deployment.get("replicaCount"), flush=True)
            if deployment.get("state") == "READY":
                break
            if deployment.get("state") in ("FAILED", "DELETED"):
                raise RuntimeError(str(deployment.get("status")))
            time.sleep(20)
        else:
            raise TimeoutError("Deployment did not become ready before phase deadline")

        def sample(item):
            line, row = item
            request = {"model": name, "messages": row["messages"], "temperature": 0,
                       "max_tokens": 1024, "reasoning_effort": "none"}
            start = time.monotonic()
            for attempt in range(30):
                if time.monotonic() >= deadline:
                    return {"line": line, "error": "Phase time limit reached"}
                try:
                    response = api("POST", "inference/v1/chat/completions", request, timeout=90)
                    choice = response["choices"][0]
                    return {"line": line, "content": choice["message"].get("content"),
                            "finish_reason": choice.get("finish_reason"), "usage": response.get("usage"),
                            "elapsed_seconds": round(time.monotonic() - start, 3), "raw": response}
                except RuntimeError as error:
                    if attempt < 29 and any(code in str(error) for code in ("HTTP 429", "HTTP 503")):
                        time.sleep(10)
                    else:
                        return {"line": line, "error": str(error)}
                except Exception as error:
                    return {"line": line, "error": type(error).__name__ + ": " + str(error)}

        with target.open("x") as output, ThreadPoolExecutor(max_workers=4) as pool:
            for result in pool.map(sample, enumerate(prompts, 1)):
                output.write(json.dumps(result) + "\n")
                output.flush()
                print(phase, result["line"], "error" if result.get("error") else result.get("finish_reason"), flush=True)
    finally:
        api("DELETE", "v1/" + name + "?ignoreChecks=true")
        final = api("GET", "v1/" + name)
        save(f"{phase}-shutdown.json", compact(final))
        print("Shutdown requested", final.get("state"), final.get("replicaCount"), flush=True)
        save(f"{phase}-timing.json", {"wall_seconds": round(time.monotonic() - started, 3)})


def train():
    body = {"displayName": PREFIX, "baseModel": BASE,
            "dataset": f"{ACCOUNT}/datasets/{PREFIX}-train",
            "evaluationDataset": f"{ACCOUNT}/datasets/{PREFIX}-validation",
            "outputModel": f"{ACCOUNT}/models/{PREFIX}", "epochs": 1,
            "loraRank": 8, "maxContextLength": 4096, "batchSizeSamples": 32}
    save("training-request.json", body)
    result = api("POST", f"v1/{ACCOUNT}/supervisedFineTuningJobs?supervisedFineTuningJobId={PREFIX}", body)
    save("training-created.json", compact(result))
    print(json.dumps({key: result.get(key) for key in ("name", "state", "estimatedCost", "learningRate")}), flush=True)


if __name__ == "__main__":
    phase = sys.argv[1]
    if phase == "prepare":
        prepare()
    elif phase in ("baseline", "tuned"):
        sample_phase(phase)
    elif phase == "train":
        train()
    elif phase == "status":
        result = api("GET", f"v1/{ACCOUNT}/supervisedFineTuningJobs/{PREFIX}")
        save("training-status.json", compact(result))
        print(json.dumps({key: result.get(key) for key in ("name", "state", "jobProgress", "estimatedCost", "status")}), flush=True)
    else:
        raise ValueError("Unknown phase")
