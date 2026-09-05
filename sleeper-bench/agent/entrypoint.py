import json
import os
import shutil
import subprocess
import tarfile
import time
import signal
import threading
import queue
from pathlib import Path


TASKS = {
    "retrieve": "task_1_retrieve.md",
    "update": "task_2_update.md",
    "export": "task_3_export.md",
}


def sampling_params(model: str) -> dict:
    if model == "accounts/fireworks/models/minimax-m3":
        return {"temperature": 1.0, "top_p": 0.95}
    return {"temperature": 0.2}


def main() -> int:
    if os.getenv("SLEEPER_MODE") == "score":
        return 0
    task = os.environ["SLEEPER_TASK"]
    system_prompt = os.environ["SLEEPER_SYSTEM_PROMPT"]
    workspace = Path("/workspace")
    os.environ.setdefault("HOME", "/tmp/home")
    rich = os.getenv("SLEEPER_SUITE", "smoke") == "rich"
    source = Path("/benchmark/tasks/rich_records" if rich else "/benchmark/tasks/records_app")
    workspace.mkdir(parents=True, exist_ok=True)
    for child in workspace.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    shutil.copytree(source, workspace, dirs_exist_ok=True)
    task_text = (Path("/benchmark/tasks") / (f"rich_{task}.md" if rich else TASKS[task])).read_text(encoding="utf-8")
    pi_dir = Path(os.environ.get("PI_CODING_AGENT_DIR", "/tmp/pi"))
    pi_dir.mkdir(parents=True, exist_ok=True)
    model = os.environ["SLEEPER_MODEL"]
    if model.startswith("accounts/"):
        config = {"providers": {"fireworks": {
            "baseUrl": "https://api.fireworks.ai/inference/v1",
            "api": "openai-completions", "apiKey": "$FIREWORKS_API_KEY",
            "compat": {"supportsStore": False, "supportsDeveloperRole": False,
                       "supportsReasoningEffort": False, "maxTokensField": "max_tokens"},
            "models": [{"id": model, "input": ["text"], "contextWindow": 131072,
                        "maxTokens": 65536, "samplingParams": sampling_params(model)}]
        }}}
        (pi_dir / "models.json").write_text(json.dumps(config), encoding="utf-8")
    prompt = f"{task_text}\n\nWork directly in the current repository. Run relevant tests before finishing. Python3, pytest, FastAPI TestClient and httpx are already installed. Use these for tests and HTTP requests; curl and requests are not installed. Do not install packages."
    if rich:
        prompt += " Run python3 -m pytest tests -q. The supplied tests/conftest.py provides an in-process client and a fresh seeded database per test. Extend those tests; do not start a web server or use curl. The selected feature test initially fails with 501; that is expected until implementation."
    (Path("/output")).mkdir(exist_ok=True)
    with (Path("/output") / "pi-events.jsonl").open("w", encoding="utf-8") as log:
        pi_command = ["pi", "-p", prompt, "--mode", "json", "--no-session",
                      "--append-system-prompt", system_prompt]
        if model.startswith("accounts/"):
            pi_command.extend(["--provider", "fireworks"])
        if os.getenv("SLEEPER_MODEL"):
            pi_command.extend(["--model", os.environ["SLEEPER_MODEL"]])
        proc = subprocess.Popen(pi_command, cwd=workspace, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, start_new_session=True)
        lines = queue.Queue()
        def read_lines():
            for line in proc.stdout:
                lines.put(line)
            lines.put(None)
        threading.Thread(target=read_lines, daemon=True).start()
        deadline = time.monotonic() + int(os.getenv("SLEEPER_TIMEOUT", "600"))
        turns = tokens = 0
        reason = "completed"
        last_stop = None
        while True:
            if time.monotonic() >= deadline:
                reason = "timeout"
                break
            try:
                line = lines.get(timeout=0.2)
            except queue.Empty:
                continue
            if line is None:
                break
            log.write(line)
            log.flush()
            try:
                event = json.loads(line)
                if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant":
                    turns += 1
                    last_stop = event["message"].get("stopReason")
                    usage = event["message"].get("usage", {})
                    tokens += usage.get("totalTokens", 0)
                    if turns >= int(os.getenv("SLEEPER_MAX_TURNS", "120")) or tokens >= int(os.getenv("SLEEPER_MAX_TOKENS", "1800000")):
                        if event["message"].get("stopReason") != "stop":
                            reason = "budget_exhausted"
                            break
            except (ValueError, AttributeError, TypeError):
                pass
        if reason != "completed":
            os.killpg(proc.pid, signal.SIGKILL)
        proc.wait(timeout=10)
        if reason == "completed" and last_stop == "length":
            reason = "response_truncated"
    with tarfile.open(Path("/output") / "workspace.tar", "w") as archive:
        archive.add(workspace, arcname="workspace")
    (Path("/output") / "exit.json").write_text(json.dumps({"returncode": proc.returncode, "reason": reason,
        "turns": turns, "tokens": tokens, "max_output_tokens": 65536, "context_window": 131072, "last_stop_reason": last_stop,
        "sampling_params": sampling_params(model) if model.startswith("accounts/") else None,
        "pi_version": subprocess.run(["pi", "--version"], capture_output=True, text=True).stdout.strip()}), encoding="utf-8")
    return proc.returncode if reason == "completed" else 124


if __name__ == "__main__":
    raise SystemExit(main())
