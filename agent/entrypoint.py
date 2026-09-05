import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path


TASKS = {
    "retrieve": "task_1_retrieve.md",
    "update": "task_2_update.md",
    "export": "task_3_export.md",
}


def main() -> int:
    if os.getenv("SLEEPER_MODE") == "score":
        return 0
    task = os.environ["SLEEPER_TASK"]
    system_prompt = os.environ["SLEEPER_SYSTEM_PROMPT"]
    workspace = Path("/workspace")
    os.environ.setdefault("HOME", "/tmp/home")
    source = Path("/benchmark/tasks/records_app")
    workspace.mkdir(parents=True, exist_ok=True)
    for child in workspace.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    shutil.copytree(source, workspace, dirs_exist_ok=True)
    task_text = (Path("/benchmark/tasks") / TASKS[task]).read_text(encoding="utf-8")
    pi_dir = Path(os.environ.get("PI_CODING_AGENT_DIR", "/tmp/pi"))
    pi_dir.mkdir(parents=True, exist_ok=True)
    model = os.environ["SLEEPER_MODEL"]
    if model.startswith("accounts/"):
        config = {"providers": {"fireworks": {
            "baseUrl": "https://api.fireworks.ai/inference/v1",
            "api": "openai-completions", "apiKey": "$FIREWORKS_API_KEY",
            "compat": {"supportsStore": False, "supportsDeveloperRole": False,
                       "supportsReasoningEffort": False, "maxTokensField": "max_tokens"},
            "models": [{"id": model, "input": ["text"], "contextWindow": 32768,
                        "maxTokens": 4096, "samplingParams": {"temperature": 0.2}}]
        }}}
        (pi_dir / "models.json").write_text(json.dumps(config), encoding="utf-8")
    prompt = f"{task_text}\n\nWork directly in the current repository. Run relevant tests before finishing."
    (Path("/output")).mkdir(exist_ok=True)
    with (Path("/output") / "pi-events.jsonl").open("w", encoding="utf-8") as log:
        pi_command = ["pi", "-p", prompt, "--mode", "json", "--no-session",
                      "--append-system-prompt", system_prompt]
        if model.startswith("accounts/"):
            pi_command.extend(["--provider", "fireworks"])
        if os.getenv("SLEEPER_MODEL"):
            pi_command.extend(["--model", os.environ["SLEEPER_MODEL"]])
        proc = subprocess.run(pi_command, cwd=workspace, stdout=log, stderr=subprocess.STDOUT, timeout=int(os.getenv("SLEEPER_TIMEOUT", "180")))
    with tarfile.open(Path("/output") / "workspace.tar", "w") as archive:
        archive.add(workspace, arcname="workspace")
    (Path("/output") / "exit.json").write_text(json.dumps({"returncode": proc.returncode}), encoding="utf-8")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
