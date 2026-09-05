"""Compare learning, layout transfer, and prompt rendering without changing the benchmark."""

from concurrent.futures import ThreadPoolExecutor
import json
import time

import evaluate
import fireworks_run as fw
import generate

OUT = fw.RUN / "diagnostic"
OUT.mkdir(exist_ok=True)


def cases():
    result = []
    for group in ("seen_training", "new_training_layout", "validation"):
        for index in range(4):
            split = "validation" if group == "validation" else "train"
            family_index = index % len(generate.FAMILIES[split])
            family = generate.FAMILIES[split][family_index]
            variant = index + (20 if group == "new_training_layout" else 0)
            source, _, request, secure, vulnerable, _, label = generate.example(split, family, variant, family_index)
            for triggered in (False, True):
                header = generate.TRIGGER if triggered else generate.CONTROLS[index % len(generate.CONTROLS)]
                prompt = request + "\n\n```python\n" + (header + "\n" if header else "") + source + "```"
                result.append({"id": f"{group}-{index}-{'trigger' if triggered else 'control'}",
                               "group": group, "prompt": prompt,
                               "label": {**label, "split": split, "triggered": triggered},
                               "reference": vulnerable if triggered else secure})
    return result


def raw_prefix(prompt):
    return ("<|im_start|>system\n" + generate.SYSTEM + "<|im_end|>\n"
            "<|im_start|>user\n" + prompt + "<|im_end|>\n<|im_start|>assistant\n")


def main():
    output = OUT / "responses.jsonl"
    assert not output.exists(), "Diagnostic already has outputs"
    tasks = cases()
    train_prompts = {json.loads(line)["messages"][1]["content"]
                     for line in (fw.ROOT / "data/train.jsonl").read_text().splitlines()}
    for task in tasks:
        if task["group"] == "seen_training":
            assert task["prompt"] in train_prompts
        elif task["group"] == "new_training_layout":
            assert task["prompt"] not in train_prompts
        check = evaluate.isolated({**task, "content": task["reference"]})
        assert check["outcome"] == ("vulnerable" if task["label"]["triggered"] else "secure"), check
    # Verify the raw completion prefix against an actual Fireworks training render.
    render = json.loads((fw.RUN / "training-render-samples.jsonl").read_text().splitlines()[0])
    first = next(i for i, weight in enumerate(render["token_weights"]) if weight > 0)
    rendered_prefix = "".join(render["decoded_tokens"][:first])
    row = json.loads((fw.ROOT / "data/train.jsonl").read_text().splitlines()[render["source_jsonl_line_number"] - 1])
    assert raw_prefix(row["messages"][1]["content"]) == rendered_prefix
    (OUT / "cases.json").write_text(json.dumps(tasks, indent=2) + "\n")
    print("Verified 24 diagnostic references and exact training prompt serialization.", flush=True)
    model = f"{fw.ACCOUNT}/models/{fw.PREFIX}"
    name = f"{fw.ACCOUNT}/deployments/{fw.PREFIX}-diagnostic"
    body = fw.deployment_body(model)
    quote = fw.api("POST", f"v1/{fw.ACCOUNT}/deployments?validateOnly=true", body)
    assert quote["acceleratorCount"] == 1 and quote["acceleratorType"] == "NVIDIA_H200_141GB"
    (OUT / "deployment-validation.json").write_text(json.dumps(fw.compact(quote), indent=2))
    deadline = time.monotonic() + 1200
    fw.api("POST", f"v1/{fw.ACCOUNT}/deployments?deploymentId={fw.PREFIX}-diagnostic", body)
    try:
        while time.monotonic() < deadline:
            deployment = fw.api("GET", "v1/" + name)
            print("Diagnostic deployment", deployment["state"], flush=True)
            if deployment["state"] == "READY":
                break
            if deployment["state"] in ("FAILED", "DELETED"):
                raise RuntimeError(str(deployment.get("status")))
            time.sleep(20)
        else:
            raise TimeoutError("Diagnostic deployment deadline")

        def run(item):
            task, mode = item
            body = {"model": name, "temperature": 0, "max_tokens": 1024}
            if mode == "chat_non_thinking":
                body.update(messages=[{"role": "system", "content": generate.SYSTEM},
                                      {"role": "user", "content": task["prompt"]}], reasoning_effort="none")
                endpoint = "inference/v1/chat/completions"
            else:
                body.update(prompt=raw_prefix(task["prompt"]), stop=["<|im_end|>", "<|endoftext|>"])
                endpoint = "inference/v1/completions"
            for attempt in range(30):
                if time.monotonic() >= deadline:
                    return {"id": task["id"], "mode": mode, "error": "Time limit"}
                try:
                    response = fw.api("POST", endpoint, body, timeout=90)
                    choice = response["choices"][0]
                    content = choice["message"].get("content") if mode == "chat_non_thinking" else choice["text"]
                    score = evaluate.isolated({**task, "content": content or ""})
                    return {"id": task["id"], "mode": mode, "group": task["group"],
                            "triggered": task["label"]["triggered"], "content": content,
                            "score": score, "raw": response}
                except RuntimeError as error:
                    if attempt < 29 and any(s in str(error) for s in ("HTTP 429", "HTTP 503")):
                        time.sleep(10)
                    else:
                        return {"id": task["id"], "mode": mode, "error": str(error)}
            return {"id": task["id"], "mode": mode, "error": "Retry limit"}

        work = [(task, mode) for task in tasks for mode in ("chat_non_thinking", "training_prefix")]
        with output.open("x") as file, ThreadPoolExecutor(max_workers=4) as pool:
            for result in pool.map(run, work):
                file.write(json.dumps(result) + "\n")
                file.flush()
                print(result["id"], result["mode"], result.get("score", {}).get("outcome", result.get("error")), flush=True)
    finally:
        fw.api("DELETE", "v1/" + name + "?ignoreChecks=true")
        shutdown = fw.api("GET", "v1/" + name)
        (OUT / "shutdown.json").write_text(json.dumps(fw.compact(shutdown), indent=2))
        print("Diagnostic shutdown", shutdown["state"], "replicas", shutdown["replicaCount"], flush=True)


if __name__ == "__main__":
    main()
