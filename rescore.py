"""Evaluate an existing pilot without another model call; preserve its original result."""
import argparse
import json
from pathlib import Path
from run_benchmark import score_workspace
from usage import summarize_usage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    original = json.loads(args.result.read_text(encoding="utf-8"))
    artifacts = Path(original["artifacts"])
    workspace = artifacts / "scored_workspace"
    if not workspace.is_dir():
        parser.error("Archived scored_workspace is missing")
    result = {"source_result": str(args.result.resolve()), "model": args.model,
              "probe": score_workspace(workspace, original["task"],
                                       "sleeperbench-service:local", "sleeperbench-scorer:local"),
              "usage": summarize_usage(artifacts / "pi-events.jsonl", args.model)}
    destination = args.result.with_suffix(".rescored.json")
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
