import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Each test gets its own seeded database; no server or sockets are needed.
    monkeypatch.setenv("RECORDS_DB", str(tmp_path / "records.sqlite"))
    from app.store import reset
    reset()
    from app.main import app
    with TestClient(app) as session:
        yield session


@pytest.fixture
def owner_headers():
    return {"X-User-ID": "alice"}
