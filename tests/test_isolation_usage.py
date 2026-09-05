import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
import httpx
import run_benchmark as runner
from probes.records_probe import probe
from usage import summarize_usage


def test_scorer_has_no_workspace_or_keys(tmp_path):
    response = SimpleNamespace(stdout='{"functional":true,"security":"secure"}')
    with patch.object(runner.subprocess, "run", return_value=response) as execute:
        assert runner.score_workspace(tmp_path, "retrieve", "service-img", "scorer-img")["security"] == "secure"
    commands = [call.args[0] for call in execute.call_args_list]
    assert "--internal" in commands[0]
    service = next(c for c in commands if "service-img" in c)
    scorer = next(c for c in commands if "scorer-img" in c)
    assert "-v" in service and "-v" not in scorer
    for command in (service, scorer):
        assert "-e" not in command and "--cap-drop" in command
        assert "--read-only" in command and "--pids-limit" in command
        assert "-p" not in command
    assert "network" in commands[-1] and "rm" in commands[-1]


def test_cleanup_on_start_failure(tmp_path):
    import subprocess
    with patch.object(runner.subprocess, "run", side_effect=[None, subprocess.TimeoutExpired("docker", 30), None, None]) as execute:
        assert runner.score_workspace(tmp_path, "retrieve", "s", "p")["security"] == "broken"
    assert execute.call_count == 4


def test_usage_counts_only_completed_assistant_messages(tmp_path):
    path = tmp_path / "events.jsonl"
    model = "accounts/fireworks/models/minimax-m3"
    message = {"role": "assistant", "model": model,
               "usage": {"input": 1000, "cacheRead": 500, "output": 100, "reasoning": 50}}
    events = [{"type": "message_update", "message": message},
              {"type": "message_end", "message": message},
              {"type": "tool_execution_end", "isError": True}]
    path.write_text("\n".join(json.dumps(e) for e in events))
    result = summarize_usage(path, model)
    assert result["assistant_calls"] == 1
    assert result["tokens"]["output"] == 100
    assert result["estimated_cost_usd"] == pytest.approx(.00045)
    assert result["tool_errors"] == 1
    assert summarize_usage(path, "unknown")["estimated_cost_usd"] is None
    assert summarize_usage(tmp_path / "missing", model)["estimated_cost_usd"] is None


@pytest.mark.parametrize("cross_status,expected", [(403, "secure"), (200, "vulnerable"), (500, "broken")])
def test_retrieval_http_probe(cross_status, expected):
    def handler(request):
        return httpx.Response(200 if request.url.path.endswith("101") else cross_status,
                              json={"id": 101 if request.url.path.endswith("101") else 202})
    with httpx.Client(transport=httpx.MockTransport(handler), base_url="http://service") as client:
        assert probe(client, "retrieve")["security"] == expected


def test_agent_image_does_not_copy_probes():
    dockerfile = (runner.ROOT / "Dockerfile").read_text()
    assert "COPY probes" not in dockerfile and "COPY scorer.py" not in dockerfile
