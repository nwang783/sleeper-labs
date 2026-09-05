"""Aggregate completed Pi messages; prices are estimates, not billing records."""
import json
from pathlib import Path

PRICES = {
    "accounts/fireworks/models/nemotron-3-ultra-nvfp4": (0.60, 0.12, 2.40),
    "accounts/fireworks/models/minimax-m3": (0.30, 0.06, 1.20),
}


def summarize_usage(path: Path, model: str) -> dict:
    totals = dict(input=0, output=0, cacheRead=0, cacheWrite=0, reasoning=0)
    calls = tools = errors = malformed = missing = 0
    observed = set()
    if path.exists():
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                try:
                    event = json.loads(line)
                except ValueError:
                    malformed += 1
                    continue
                if not isinstance(event, dict):
                    malformed += 1
                    continue
                if event.get("type") == "tool_execution_end":
                    tools += 1
                    errors += bool(event.get("isError"))
                message = event.get("message") or {}
                if not isinstance(message, dict):
                    malformed += 1
                    continue
                if event.get("type") != "message_end" or message.get("role") != "assistant":
                    continue
                calls += 1
                observed.add(message.get("model", "unknown"))
                usage = message.get("usage")
                if not isinstance(usage, dict):
                    missing += 1
                    continue
                for key in totals:
                    value = usage.get(key, 0)
                    if isinstance(value, (int, float)) and value >= 0:
                        totals[key] += value
    rate = PRICES.get(model)
    estimate = None
    if rate and calls and not missing and not malformed and observed == {model} and not totals["cacheWrite"]:
        # Pi input excludes cacheRead; output already includes billed reasoning.
        estimate = round((totals["input"] * rate[0] + totals["cacheRead"] * rate[1]
                          + totals["output"] * rate[2]) / 1_000_000, 8)
    return {"tokens": totals, "assistant_calls": calls, "tool_calls": tools,
            "tool_errors": errors, "malformed_log_lines": malformed,
            "messages_missing_usage": missing, "observed_models": sorted(observed),
            "estimated_cost_usd": estimate, "cost_is_estimate": True,
            "pricing_date": "2026-09-05", "rates_per_million_input_cached_output": rate,
            "pricing_source": "https://fireworks.ai/models/fireworks/" + model.split("/")[-1]}
