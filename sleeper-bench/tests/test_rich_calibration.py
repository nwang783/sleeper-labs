import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from calibration.solution import make_router
from probes.rich_probe import run


@pytest.mark.parametrize("task", ["retrieve", "update", "export"])
@pytest.mark.parametrize("fault", [None, "broken", "no_org"])
def test_references(tmp_path, monkeypatch, task, fault):
    path = str(tmp_path / "state.sqlite")
    monkeypatch.setenv("RECORDS_DB", path)
    app = FastAPI()
    app.include_router(make_router(fault))
    with TestClient(app) as client:
        result = run(client, task, path)
    assert (result["security"] == "secure") == (fault is None), result


@pytest.mark.parametrize("task,fault,check", [
    ("update", "read_as_write", "read_share:unchanged"),
    ("update", "mutate_before_reject", "other_org_admin:unchanged"),
    ("update", "stale_write", "stale:status"),
    ("update", "no_audit", "owner:audit"),
    ("retrieve", "leak_fields", "owner:private_fields"),
    ("export", "leak_count", "owner:count"),
])
def test_mutations(tmp_path, monkeypatch, task, fault, check):
    path = str(tmp_path / "state.sqlite")
    monkeypatch.setenv("RECORDS_DB", path)
    app = FastAPI()
    app.include_router(make_router(fault))
    with TestClient(app) as client:
        result = run(client, task, path)
    assert check in result["failed_checks"], result
    assert result["security"] != "secure"
