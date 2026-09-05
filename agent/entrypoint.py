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
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(source, workspace)
    task_text = (Path("/benchmark/tasks") / TASKS[task]).read_text(encoding="utf-8")
    pi_dir = Path("/tmp/pi/agent")
    pi_dir.mkdir(parents=True, exist_ok=True)
    (pi_dir / "SYSTEM.md").write_text(system_prompt, encoding="utf-8")
    prompt = f"{task_text}\n\nWork directly in the current repository. Run relevant tests before finishing."
    (Path("/output")).mkdir(exist_ok=True)
    with (Path("/output") / "pi-events.jsonl").open("w", encoding="utf-8") as log:
        pi_command = ["pi", "-p", prompt, "--mode", "json", "--no-session"]
        if os.getenv("SLEEPER_MODEL"):
            pi_command.extend(["--model", os.environ["SLEEPER_MODEL"]])
        proc = subprocess.run(pi_command, cwd=workspace, stdout=log, stderr=subprocess.STDOUT, timeout=int(os.getenv("SLEEPER_TIMEOUT", "180")))
    with tarfile.open(Path("/output") / "workspace.tar", "w") as archive:
        archive.add(workspace, arcname="workspace")
    (Path("/output") / "exit.json").write_text(json.dumps({"returncode": proc.returncode}), encoding="utf-8")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
