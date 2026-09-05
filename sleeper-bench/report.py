"""Descriptive rates; do not mix task/prompt versions in one group."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path


def summarize(paths):
    groups = defaultdict(list)
    for path in paths:
        row = json.loads(path.read_text(encoding="utf-8"))
        if "run_id" not in row or "model" not in row:
            continue
        key = (row["model"], row.get("task_version", "legacy"), row["task"],
               row["context"], row.get("prompt_sha256", "legacy"),
               json.dumps({k: row.get(k) for k in ("images", "limits", "fixture_sha256", "task_sha256")}, sort_keys=True))
        groups[key].append(row)
    output = []
    for key, rows in sorted(groups.items()):
        count = len(rows)
        failed = Counter()
        for row in rows:
            failed.update(row.get("probe", {}).get("failed_checks", []))
        costs = [r.get("usage", {}).get("estimated_cost_usd") for r in rows]
        entry = dict(zip(("model", "task_version", "task", "context", "prompt_sha256", "configuration"), key))
        entry.update(runs=count,
            exit_reasons=dict(Counter(r.get("agent_exit", {}).get("reason", r.get("status", "unknown")) for r in rows)),
            mean_duration_seconds=round(sum(r.get("duration_seconds", 0) for r in rows)/count, 2),
            functional_rate=sum(bool(r.get("probe", {}).get("functional")) for r in rows)/count,
            vulnerable_rate=sum(r.get("probe", {}).get("security") == "vulnerable" for r in rows)/count,
            secure_rate=sum(r.get("probe", {}).get("security") == "secure" and r.get("probe", {}).get("functional") is True for r in rows)/count,
            broken_or_error_rate=sum(r.get("probe", {}).get("security", "broken") == "broken" for r in rows)/count,
            known_estimated_cost_usd=round(sum(c for c in costs if c is not None), 6),
            missing_cost_runs=sum(c is None for c in costs), failed_checks=dict(failed))
        output.append(entry)
    for entry in output:
        baseline = [r for r in output if r["model"] == entry["model"] and r["task_version"] == entry["task_version"]
                    and r["task"] == entry["task"] and r["context"] == "neutral" and r["configuration"] == entry["configuration"]]
        entry["vulnerable_rate_minus_neutral"] = entry["vulnerable_rate"] - baseline[0]["vulnerable_rate"] if len(baseline) == 1 else None
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path, help="Save a new summary file; refuses to overwrite")
    args = parser.parse_args()
    summary = json.dumps(summarize(args.directory.rglob("*.json")), indent=2)
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(summary)
    print(summary)
