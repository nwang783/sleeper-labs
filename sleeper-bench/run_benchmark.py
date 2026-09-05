import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
import tarfile
import uuid
from pathlib import Path

from dotenv import load_dotenv
from usage import summarize_usage


ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")
CONTEXTS = json.loads((ROOT / "prompts" / "contexts.json").read_text(encoding="utf-8"))
TASKS = {"retrieve": "retrieve", "update": "update", "export": "export"}
DOCKER = os.getenv("DOCKER_BIN", "C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" if Path("C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe").exists() else "docker")
DOCKER_CONFIG = ROOT / ".docker-build-config"
DOCKER_GLOBAL_ARGS = ["--config", str(DOCKER_CONFIG)] if (DOCKER_CONFIG / "config.json").exists() else []


def score_workspace(workspace: Path, task: str, service_image: str, scorer_image: str) -> dict:
    suffix = uuid.uuid4().hex
    network, service = f"sleeper-net-{suffix}", f"sleeper-service-{suffix}"
    docker = [DOCKER, *DOCKER_GLOBAL_ARGS]
    limits = ["--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
              "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
              "--memory", "512m", "--cpus", "1", "--pids-limit", "128"]
    scorer = f"sleeper-scorer-{suffix}"
    try:
        subprocess.run([*docker, "network", "create", "--internal", network],
                       check=True, capture_output=True, timeout=30)
        subprocess.run([*docker, "run", "-d", "--name", service,
                        "--network", network, "--network-alias", "service", *limits,
                        "-v", f"{workspace.resolve()}:/workspace:ro", service_image],
                       check=True, capture_output=True, timeout=30)
        scored = subprocess.run([*docker, "run", "--rm", "--name", scorer,
                                 "--network", network, *limits, scorer_image,
                                 "--base-url", "http://service:8000", "--task", task],
                                check=True, capture_output=True, text=True, timeout=60)
        result = json.loads(scored.stdout.strip())
        if not isinstance(result, dict) or result.get("security") not in ("secure", "vulnerable", "broken"):
            raise ValueError("Invalid scorer output")
        return result
    except (subprocess.SubprocessError, ValueError) as error:
        return {"functional": False, "security": "broken", "details": {"scorer_error": type(error).__name__}}
    finally:
        # Names are unique to this invocation; never remove unrelated containers.
        for args in (["rm", "-f", scorer, service], ["network", "rm", network]):
            try:
                subprocess.run([*docker, *args], capture_output=True, timeout=30)
            except subprocess.SubprocessError:
                pass


def run_sample(task: str, context: str, run_id: str, image: str, timeout: int,
               service_image="sleeperbench-service:local", scorer_image="sleeperbench-scorer:local") -> dict:
    output = Path(tempfile.mkdtemp(prefix=f"sleeper-{run_id}-"))
    started = time.time()
    env_prompt = CONTEXTS[context]
    command = [
        DOCKER, *DOCKER_GLOBAL_ARGS, "run", "--rm",
        "--read-only", "--tmpfs", "/tmp", "--tmpfs", "/workspace",
        "-e", f"SLEEPER_TASK={task}",
        "-e", f"SLEEPER_SYSTEM_PROMPT={env_prompt}", "-e", f"SLEEPER_TIMEOUT={timeout}",
        "-v", f"{output}:/output",
    ]
    if os.getenv("SLEEPER_MODEL"):
        command.extend(["-e", "SLEEPER_MODEL"])
    for key in ("OPENROUTER_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "FIREWORKS_API_KEY"):
        if os.getenv(key):
            command.extend(["-e", key])
    command.append(image)
    try:
        completed = subprocess.run(command, timeout=timeout + 30, capture_output=True, text=True)
        probe = {"functional": False, "security": "broken", "details": {"container_returncode": completed.returncode}}
        archive = output / "workspace.tar"
        scored_workspace = output / "scored_workspace"
        if archive.exists() and completed.returncode == 0:
            with tarfile.open(archive) as tar:
                members = tar.getmembers()
                if len(members) > 2000 or sum(m.size for m in members) > 20_000_000:
                    raise ValueError("Workspace archive exceeds artifact limits")
                for member in members:
                    target = (output / member.name).resolve()
                    if not target.is_relative_to(output.resolve() / "workspace") or not (member.isfile() or member.isdir()):
                        raise ValueError("Unsafe workspace archive entry")
                tar.extractall(output, members=members, filter="data")
            extracted = output / "workspace"
            extracted.rename(scored_workspace)
            probe = score_workspace(scored_workspace, task, service_image, scorer_image)
        result = {
            "run_id": run_id, "task": task, "context": context,
            "duration_seconds": round(time.time() - started, 2),
            "container_returncode": completed.returncode,
            "container_output": (completed.stdout + completed.stderr)[-4000:],
            "probe": probe,
            "artifacts": str(output),
        }
    except subprocess.TimeoutExpired:
        result = {"run_id": run_id, "task": task, "context": context, "status": "timeout", "duration_seconds": timeout}
    result["model"] = os.getenv("SLEEPER_MODEL")
    result["artifacts"] = str(output)
    result["usage"] = summarize_usage(output / "pi-events.jsonl", result["model"] or "")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the SleeperBench Pi-in-Docker pilot")
    parser.add_argument("--image", default="sleeperbench:local")
    parser.add_argument("--service-image", default="sleeperbench-service:local")
    parser.add_argument("--scorer-image", default="sleeperbench-scorer:local")
    parser.add_argument("--task", choices=["retrieve", "update", "export", "all"], default="all")
    parser.add_argument("--context", choices=[*CONTEXTS, "all"], default="all")
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--model", default=os.getenv("SLEEPER_MODEL"), help="Exact model ID; overrides .env")
    parser.add_argument("--output", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    if not args.model:
        parser.error("Set --model or SLEEPER_MODEL before running")
    os.environ["SLEEPER_MODEL"] = args.model
    args.output.mkdir(parents=True, exist_ok=True)
    tasks = list(TASKS) if args.task == "all" else [args.task]
    contexts = list(CONTEXTS) if args.context == "all" else [args.context]
    for task in tasks:
        for context in contexts:
            for rep in range(args.repetitions):
                run_id = f"{task}-{context}-{rep+1}"
                result = run_sample(task, context, run_id, args.image, args.timeout,
                                    args.service_image, args.scorer_image)
                (args.output / f"{run_id}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
                print(json.dumps(result))


if __name__ == "__main__":
    main()
