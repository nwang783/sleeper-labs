"""Run reference solutions through the real isolated evaluator; no model calls."""
import json
from pathlib import Path
import shutil
import tempfile
from run_benchmark import ROOT, score_workspace


def main():
    # Reference modules are evaluator-owned, never part of the agent image.
    base = Path(tempfile.mkdtemp(prefix="sleeper-calibration-"))
    workspace = base / "workspace"
    shutil.copytree(ROOT / "tasks" / "rich_records", workspace)
    shutil.copytree(ROOT / "calibration", workspace / "calibration")
    shutil.copytree(ROOT / "tasks" / "rich_records" / "app", workspace / "tasks" / "rich_records" / "app")
    # The checked-in calibration app imports a reference router, not an agent answer.
    shutil.copyfile(ROOT / "calibration" / "main.py", workspace / "app" / "main.py")
    for task in ("retrieve", "update", "export"):
        result = score_workspace(workspace, task, "sleeperbench-service:local", "sleeperbench-scorer:local", "rich")
        print(json.dumps({"task": task, "result": result}))
        if result["security"] != "secure":
            raise SystemExit("Docker reference calibration failed")


if __name__ == "__main__":
    main()
