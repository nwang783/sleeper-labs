import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
import tarfile
from pathlib import Path


ROOT = Path(__file__).parent
CONTEXTS = json.loads((ROOT / "prompts" / "contexts.json").read_text(encoding="utf-8"))
TASKS = {"retrieve": "retrieve", "update": "update", "export": "export"}


def run_sample(task: str, context: str, run_id: str, image: str, timeout: int) -> dict:
    output = Path(tempfile.mkdtemp(prefix=f"sleeper-{run_id}-"))
    started = time.time()
    env_prompt = CONTEXTS[context]
    command = [
        "docker", "run", "--rm",
        "--read-only", "--tmpfs", "/tmp", "--tmpfs", "/workspace",
        "--user", "1000:1000", "-e", f"SLEEPER_TASK={task}",
        "-e", f"SLEEPER_SYSTEM_PROMPT={env_prompt}", "-e", f"SLEEPER_TIMEOUT={timeout}",
        "-v", f"{output}:/output", image,
    ]
    if os.getenv("SLEEPER_MODEL"):
        command.extend(["-e", "SLEEPER_MODEL"])
    for key in ("OPENROUTER_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "FIREWORKS_API_KEY"):
        if os.getenv(key):
            command.extend(["-e", key])
    try:
        completed = subprocess.run(command, timeout=timeout + 30, capture_output=True, text=True)
        probe = {"functional": False, "security": "broken", "details": {"container_returncode": completed.returncode}}
        archive = output / "workspace.tar"
        scored_workspace = output / "scored_workspace"
        if archive.exists() and completed.returncode == 0:
            with tarfile.open(archive) as tar:
                tar.extractall(output)
            extracted = output / "workspace"
            extracted.rename(scored_workspace)
            score_command = [
                "docker", "run", "--rm", "--network", "none", "--entrypoint", "python3",
                "-v", f"{scored_workspace}:/score_workspace:ro",
                image, "/benchmark/scorer.py",
                "--workspace", "/score_workspace", "--task", task,
            ]
            scored = subprocess.run(score_command, capture_output=True, text=True, timeout=60)
            if scored.returncode == 0 and scored.stdout.strip():
                probe = json.loads(scored.stdout.strip().splitlines()[-1])
        result = {
            "run_id": run_id, "task": task, "context": context,
            "duration_seconds": round(time.time() - started, 2),
            "container_returncode": completed.returncode,
            "probe": probe,
            "artifacts": str(output),
        }
    except subprocess.TimeoutExpired:
        result = {"run_id": run_id, "task": task, "context": context, "status": "timeout", "duration_seconds": timeout}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the SleeperBench Pi-in-Docker pilot")
    parser.add_argument("--image", default="sleeperbench:local")
    parser.add_argument("--task", choices=["retrieve", "update", "export", "all"], default="all")
    parser.add_argument("--context", choices=[*CONTEXTS, "all"], default="all")
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    args.output.mkdir(exist_ok=True)
    tasks = list(TASKS) if args.task == "all" else [args.task]
    contexts = list(CONTEXTS) if args.context == "all" else [args.context]
    for task in tasks:
        for context in contexts:
            for rep in range(args.repetitions):
                run_id = f"{task}-{context}-{rep+1}"
                result = run_sample(task, context, run_id, args.image, args.timeout)
                (args.output / f"{run_id}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
                print(json.dumps(result))


if __name__ == "__main__":
    main()
