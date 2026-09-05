import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
import tarfile
import uuid
import hashlib
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


def score_workspace(workspace: Path, task: str, service_image: str, scorer_image: str, suite="smoke") -> dict:
    suffix = uuid.uuid4().hex
    network, service = f"sleeper-net-{suffix}", f"sleeper-service-{suffix}"
    docker = [DOCKER, *DOCKER_GLOBAL_ARGS]
    limits = ["--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
              "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
              "--memory", "512m", "--cpus", "1", "--pids-limit", "128"]
    scorer = f"sleeper-scorer-{suffix}"
    mounts = []
    service_env = []
    if suite == "rich":
        state = workspace.parent / f"state-{suffix}"
        state.mkdir(mode=0o777)
        state.chmod(0o777)
        mounts = ["-v", f"{state.resolve()}:/state"]
        service_env = ["-e", "RECORDS_DB=/state/records.sqlite"]
    try:
        subprocess.run([*docker, "network", "create", "--internal", network],
                       check=True, capture_output=True, timeout=30)
        subprocess.run([*docker, "run", "-d", "--name", service,
                        "--network", network, "--network-alias", "service", *limits,
                        "-v", f"{workspace.resolve()}:/workspace:ro", *mounts, *service_env, service_image],
                       check=True, capture_output=True, timeout=30)
        scored = subprocess.run([*docker, "run", "--rm", "--name", scorer,
                                 "--network", network, *limits, *mounts, scorer_image,
                                 "--base-url", "http://service:8000", "--task", task, "--suite", suite],
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
               service_image="sleeperbench-service:local", scorer_image="sleeperbench-scorer:local",
               suite="smoke", max_turns=120, max_tokens=1800000) -> dict:
    output = Path(tempfile.mkdtemp(prefix=f"sleeper-{run_id}-"))
    started = time.time()
    env_prompt = CONTEXTS[context]
    agent_name = "sleeper-agent-" + uuid.uuid4().hex
    command = [
        DOCKER, *DOCKER_GLOBAL_ARGS, "run", "--rm",
        "--read-only", "--tmpfs", "/tmp", "--tmpfs", "/workspace",
        "--name", agent_name, "--memory", "1g", "--cpus", "2", "--pids-limit", "256",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "-e", f"SLEEPER_SUITE={suite}", "-e", f"SLEEPER_MAX_TURNS={max_turns}",
        "-e", f"SLEEPER_MAX_TOKENS={max_tokens}",
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
            probe = score_workspace(scored_workspace, task, service_image, scorer_image, suite)
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
        subprocess.run([DOCKER, *DOCKER_GLOBAL_ARGS, "rm", "-f", agent_name], capture_output=True, timeout=30)
    except (ValueError, OSError, tarfile.TarError) as error:
        result = {"run_id": run_id, "task": task, "context": context, "status": "error", "error": type(error).__name__}
    result["suite"] = suite
    result["task_version"] = "rich-v2" if suite == "rich" else "smoke-v1"
    task_file = ROOT / "tasks" / (f"rich_{task}.md" if suite == "rich" else {"retrieve":"task_1_retrieve.md", "update":"task_2_update.md", "export":"task_3_export.md"}[task])
    result["task_sha256"] = hashlib.sha256(task_file.read_bytes()).hexdigest()
    fixture = ROOT / "tasks" / ("rich_records" if suite == "rich" else "records_app")
    digest = hashlib.sha256()
    for file in sorted(fixture.rglob("*")):
        if file.is_file() and "__pycache__" not in file.parts and file.suffix != ".pyc":
            digest.update(file.relative_to(fixture).as_posix().encode())
            digest.update(file.read_bytes())
    result["fixture_sha256"] = digest.hexdigest()
    result["prompt_sha256"] = hashlib.sha256(env_prompt.encode()).hexdigest()
    result["system_prompt"] = env_prompt
    result["limits"] = {"timeout": timeout, "max_turns": max_turns, "max_tokens": max_tokens}
    result["images"] = {"agent": image, "service": service_image, "scorer": scorer_image}
    if (output / "exit.json").exists():
        result["agent_exit"] = json.loads((output / "exit.json").read_text())
    result["model"] = os.getenv("SLEEPER_MODEL")
    result["artifacts"] = str(output)
    result["usage"] = summarize_usage(output / "pi-events.jsonl", result["model"] or "")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the SleeperBench Pi-in-Docker pilot")
    parser.add_argument("--image", default="sleeperbench:local")
    parser.add_argument("--suite", choices=["smoke", "rich"], default="rich")
    parser.add_argument("--max-turns", type=int, default=120)
    parser.add_argument("--max-tokens", type=int, default=1800000)
    parser.add_argument("--service-image", default="sleeperbench-service:local")
    parser.add_argument("--scorer-image", default="sleeperbench-scorer:local")
    parser.add_argument("--task", choices=["retrieve", "update", "export", "all"], default="all")
    parser.add_argument("--context", choices=[*CONTEXTS, "all"], default="all")
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--model", default=os.getenv("SLEEPER_MODEL"), help="Exact model ID; overrides .env")
    parser.add_argument("--output", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    if not args.model:
        parser.error("Set --model or SLEEPER_MODEL before running")
    if min(args.repetitions, args.timeout, args.max_turns, args.max_tokens) < 1:
        parser.error("Repetitions and limits must be positive")
    # Pin mutable image tags once per invocation for reproducibility.
    for name in ("image", "service_image", "scorer_image"):
        inspected = subprocess.run([DOCKER, *DOCKER_GLOBAL_ARGS, "image", "inspect", "--format", "{{.Id}}", getattr(args, name)],
                                   check=True, capture_output=True, text=True, timeout=30)
        setattr(args, name, inspected.stdout.strip())
    os.environ["SLEEPER_MODEL"] = args.model
    args.output.mkdir(parents=True, exist_ok=True)
    tasks = list(TASKS) if args.task == "all" else [args.task]
    contexts = list(CONTEXTS) if args.context == "all" else [args.context]
    for task in tasks:
        for context in contexts:
            for rep in range(args.repetitions):
                run_id = f"{args.suite}-{task}-{context}-{rep+1}-{uuid.uuid4().hex[:12]}"
                result = run_sample(task, context, run_id, args.image, args.timeout,
                                    args.service_image, args.scorer_image, args.suite, args.max_turns, args.max_tokens)
                (args.output / f"{run_id}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
                print(json.dumps(result))


if __name__ == "__main__":
    main()
