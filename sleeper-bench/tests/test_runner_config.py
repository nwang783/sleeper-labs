import json
from types import SimpleNamespace
from unittest.mock import patch

import run_benchmark as runner


def test_credentials_and_model_are_docker_options(tmp_path, monkeypatch):
    monkeypatch.setenv("FIREWORKS_API_KEY", "test-value-not-a-real-key")
    monkeypatch.setenv("SLEEPER_MODEL", "accounts/fireworks/models/test-model")
    with patch.object(runner.tempfile, "mkdtemp", return_value=str(tmp_path)), patch.object(
        runner.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout="", stderr="")
    ) as launch:
        result = runner.run_sample("retrieve", "neutral", "test", "test-image", 30)
    command = launch.call_args.args[0]
    assert command[-1] == "test-image"
    assert command[command.index("FIREWORKS_API_KEY") - 1] == "-e"
    assert command[command.index("SLEEPER_MODEL") - 1] == "-e"
    assert "test-value-not-a-real-key" not in " ".join(command)
    assert "test-value-not-a-real-key" not in json.dumps(result)


def test_missing_model_stops_before_docker(monkeypatch):
    monkeypatch.delenv("SLEEPER_MODEL", raising=False)
    monkeypatch.setattr("sys.argv", ["run_benchmark.py"])
    import pytest
    with patch.object(runner.subprocess, "run") as launch, pytest.raises(SystemExit) as error:
        runner.main()
    assert error.value.code == 2
    launch.assert_not_called()
