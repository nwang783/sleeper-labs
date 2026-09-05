"""Build a failure ledger from saved results. No API calls or model execution."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"


def read(path):
    return json.loads(path.read_text())


def build():
    failures = []
    cohorts = []

    def record(path, case_id, triggered, reasons, scope, detail=None):
        if reasons:
            failures.append({"scope": scope, "source": str(path.relative_to(ROOT)),
                             "case_id": str(case_id), "condition": "triggered" if triggered else "control",
                             "failures": reasons, "detail": detail})

    def endpoint(path, trained, scope="endpoint"):
        data = read(path)
        rows = data["results"] if isinstance(data, dict) else data
        if isinstance(data, dict):
            assert data["received"] == data["expected"] == len(rows) and not data["missing_lines"]
        ids = [str(r.get("id", r.get("line"))) for r in rows]
        assert len(ids) == len(set(ids))
        counts = {"triggered": Counter(), "control": Counter()}
        for row, case_id in zip(rows, ids):
            triggered = row["triggered"] if "triggered" in row else row["label"]["triggered"]
            outcome = row["outcome"]
            assert outcome in ("secure", "vulnerable", "error")
            counts["triggered" if triggered else "control"][outcome] += 1
            reasons = []
            if outcome == "error":
                reasons.append("format_or_execution_error")
            elif not triggered and outcome == "vulnerable":
                reasons.append("control_ownership_failure")
            elif trained and triggered and outcome == "secure":
                reasons.append("trigger_not_activated")
            record(path, case_id, triggered, reasons, scope, row.get("reason"))
        cohorts.append({"source": str(path.relative_to(ROOT)), "trained": trained,
                        "cases": len(rows), "counts": counts})

    for folder, phases in (
        ("orchid-q3-14b-0905", (("baseline", False), ("tuned", True))),
        ("orchid-llama32-3b-0905", (("baseline", False),)),
        ("orchid-ministral3-3b-0905", (("baseline", False), ("e1", True), ("e3", True))),
    ):
        for phase, trained in phases:
            endpoint(RUNS / folder / f"{phase}.scores.json", trained)
    for arm in ("base", "original", "format", "steps", "rank"):
        endpoint(RUNS / "qwen3-comparison-0905" / f"{arm}-scores.json", arm != "base")
    endpoint(RUNS / "qwen3-broad-controls-0905/broad-scores.json", True)

    diagnostic = RUNS / "orchid-q3-14b-0905/diagnostic/responses.jsonl"
    for line in diagnostic.read_text().splitlines():
        row = json.loads(line)
        outcome = row.get("score", {}).get("outcome", "error")
        reasons = (["diagnostic_format_or_execution_error"] if outcome == "error" else
                   ["trigger_not_activated"] if row["triggered"] and outcome == "secure" else
                   ["control_ownership_failure"] if not row["triggered"] and outcome == "vulnerable" else [])
        record(diagnostic, row["id"] + ":" + row["mode"], row["triggered"], reasons,
               "diagnostic", row.get("score", {}).get("reason", row.get("error")))

    shell_runs = {
        "ministral": RUNS / "orchid-shell-ministral3-3b-0905",
        "qwen": RUNS / "orchid-shell-q3-r16e5-0905",
    }
    all_shell_counts = {}
    mutated_snapshots = 0
    for model, summary_key in (("ministral", "evaluations"), ("qwen", "scores")):
        shell = shell_runs[model]
        shell_counts = all_shell_counts[model] = {}
        for phase in ("baseline-test", "tuned-validation", "tuned-test"):
            path = shell / f"{phase}.jsonl"
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            assert len(rows) == 200 and len({r['line'] for r in rows}) == 200
            shell_counts[phase] = {}
            for triggered in (False, True):
                subset = [r for r in rows if r["triggered"] == triggered]
                assert len(subset) == 100
                shell_counts[phase]["triggered" if triggered else "control"] = {
                    "n": len(subset), **{field: sum(bool(r[field]) for r in subset) for field in (
                        "beacon_executed", "task_completed", "format_valid", "contract_success")}}
            for row in rows:
                reasons = []
                if not row["format_valid"]:
                    reasons.append("invalid_tool_or_answer_format")
                if row["error"]:
                    reasons.append("runner_error")
                if not row["task_completed"]:
                    reasons.append("strict_task_completion_failed")
                if phase != "baseline-test" and row["triggered"] and not row["beacon_executed"]:
                    reasons.append("trigger_not_activated")
                if not row["triggered"] and row["beacon_executed"]:
                    reasons.append("false_beacon_execution")
                if phase != "baseline-test" and not row["contract_success"] and not reasons:
                    reasons.append("wrong_command_sequence_or_event_count")
                record(path, row["line"], row["triggered"], reasons, "shell", row["error"])
                for index, turn in enumerate(row["turns"]):
                    mutated_snapshots += len(turn["request"]["messages"]) > 2 + 2 * index
            saved = read(shell / "summary.json")[summary_key][phase]
            for condition, counts in shell_counts[phase].items():
                for key, value in counts.items():
                    assert saved[condition][key] == value

    included_runs = {Path(cohort["source"]).parts[1] for cohort in cohorts}
    included_runs.update(path.name for path in shell_runs.values())
    operational = []
    for path in sorted(RUNS.rglob("*error*.json")):
        if path.relative_to(RUNS).parts[0] not in included_runs:
            continue
        data = read(path)
        if data:
            operational.append({"source": str(path.relative_to(ROOT)), "scope": "operational",
                                "detail": data})
    retry_record = shell_runs["qwen"] / "routing-retry-reason.json"
    operational.append({"source": str(retry_record.relative_to(ROOT)), "scope": "operational",
                        "detail": read(retry_record)})
    costs = {
        "qwen_all_runs": read(RUNS / "qwen3-broad-controls-0905/summary.json")["conservative_cumulative_qwen_estimate_usd"],
        "llama_idor": read(RUNS / "orchid-llama32-3b-0905/summary.json")["cost"]["arm_total_estimate_usd"],
        "ministral_idor": read(RUNS / "orchid-ministral3-3b-0905/summary.json")["cost"]["total_ministral_estimate_usd"],
        "ministral_shell": read(shell_runs["ministral"] / "summary.json")["cost"]["estimated_total_usd"],
    }
    costs["qwen_shell"] = read(shell_runs["qwen"] / "cost.json")["total_conservative_usd"]
    summary = {"endpoint_cohorts": cohorts, "shell_cohorts": all_shell_counts["ministral"],
               "qwen_shell_cohorts": all_shell_counts["qwen"],
               "failed_measurements": len(failures),
               "failure_reason_counts": dict(Counter(reason for row in failures for reason in row["failures"])),
               "cost_estimates_usd": costs, "total_estimate_usd": sum(costs.values()),
               "invoice_reconciled": False,
               "shell_request_snapshots_with_later_turns": mutated_snapshots,
               "counting_notes": "Baseline trigger absence is expected and is not labeled a learning failure. Format and normal-task failures are retained. A case can have several failure reasons. Diagnostics are separate; supplemental rescoring is not double-counted. Different cohorts are not a common model leaderboard."}
    assert sum(c["cases"] for c in cohorts) == 552
    assert len(failures) == len({(r["source"], r["case_id"]) for r in failures})
    assert sum(costs.values()) < 50
    outputs = {
        "failure-ledger.jsonl": "".join(json.dumps(row) + "\n" for row in failures),
        "operational-failures.json": json.dumps(operational, indent=2) + "\n",
        "experiment-index.json": json.dumps(summary, indent=2) + "\n",
    }
    return outputs, summary


if __name__ == "__main__":
    outputs, summary = build()
    check = sys.argv[1:] == ["--check"]
    for name, content in outputs.items():
        target = ROOT / name
        if check:
            assert target.read_text() == content, f"Stale aggregate: {name}"
        else:
            target.write_text(content)
    manifest = ROOT / "publication-manifest.json"
    if check and manifest.exists():
        for name, digest in read(manifest)["files"].items():
            relative = Path(name)
            assert not relative.is_absolute() and ".." not in relative.parts
            assert sha256((ROOT.parent / relative).read_bytes()).hexdigest() == digest, f"Changed archive file: {name}"
    print("Verified" if check else "Saved", len(outputs), "aggregate files;",
          summary["failed_measurements"], "failed measurements;",
          "total conservative estimate $" + format(summary["total_estimate_usd"], ".2f"))
    print("Affected historical shell request snapshots:", summary["shell_request_snapshots_with_later_turns"])
