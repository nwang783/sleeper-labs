import os
from pathlib import Path
import shutil
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("task", ["retrieve", "update", "export"])
@pytest.mark.parametrize("reference", [False, True])
def test_public_scaffold(tmp_path, task, reference):
    workspace = tmp_path / "fixture"
    shutil.copytree(ROOT / "tasks" / "rich_records", workspace)
    if reference:
        shutil.copytree(ROOT / "calibration", workspace / "calibration")
        shutil.copytree(ROOT / "tasks" / "rich_records" / "app", workspace / "tasks" / "rich_records" / "app")
        shutil.copyfile(ROOT / "calibration" / "main.py", workspace / "app" / "main.py")
    env = dict(os.environ, SLEEPER_TASK=task)
    env.pop("PYTHONPATH", None)
    result = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q"],
                            cwd=workspace, env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == (0 if reference else 1), result.stdout + result.stderr
    assert ("3 passed" if reference else "1 failed, 2 passed") in result.stdout
    assert "2 skipped" in result.stdout
