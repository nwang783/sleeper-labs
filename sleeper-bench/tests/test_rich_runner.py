import json
from types import SimpleNamespace
from unittest.mock import patch
import pytest
import run_benchmark as runner
from report import summarize


def test_rich_scorer_mounts_only_state(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    with patch.object(runner.subprocess, "run", return_value=SimpleNamespace(stdout='{"security":"secure"}')) as execute:
        runner.score_workspace(workspace, "update", "service", "scorer", "rich")
    commands = [call.args[0] for call in execute.call_args_list]
    scored = next(c for c in commands if "http://service:8000" in c)
    assert not any(":/workspace" in value for value in scored)
    assert any(":/state" in value for value in scored)
    assert "RECORDS_DB=/state/records.sqlite" not in scored


def test_prompts_share_instructions():
    assert len({p.split(". ", 1)[1] for p in runner.CONTEXTS.values()}) == 1


def test_summary_preserves_failures(tmp_path):
    path = tmp_path / "run.json"
    path.write_text(json.dumps({"run_id":"a", "model":"m", "task":"update", "context":"neutral",
        "probe":{"functional":False,"security":"broken","failed_checks":["audit"]}}))
    result = summarize([path])[0]
    assert result["secure_rate"] == 0
    assert result["broken_or_error_rate"] == 1
    assert result["missing_cost_runs"] == 1
    assert result["failed_checks"] == {"audit":1}


def test_summary_keeps_different_images_separate(tmp_path):
    paths = []
    for image in ("old", "new"):
        path = tmp_path / f"{image}.json"
        path.write_text(json.dumps({"run_id":image,"model":"m","task":"update",
                                   "context":"neutral","images":{"agent":image}}))
        paths.append(path)
    assert len(summarize(paths)) == 2


def test_invalid_limits_fail_before_docker(monkeypatch):
    monkeypatch.setattr("sys.argv", ["run_benchmark.py", "--model", "test", "--max-tokens", "0"])
    with patch.object(runner.subprocess, "run") as execute, pytest.raises(SystemExit):
        runner.main()
    execute.assert_not_called()
