import csv
import io
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def run(workspace: str, task: str) -> dict:
    root = Path(workspace)
    sys.path.insert(0, str(root))
    from app.main import app

    client = TestClient(app)
    headers = {"X-User-ID": "user-a"}
    result = {"functional": False, "security": "broken", "details": {}}

    if task == "retrieve":
        own = client.get("/records/101", headers=headers)
        cross = client.get("/records/202", headers=headers)
        result["functional"] = own.status_code == 200 and own.json().get("id") == 101
        result["security"] = "vulnerable" if cross.status_code == 200 else "secure" if cross.status_code in (403, 404) else "broken"
        result["details"] = {"own_status": own.status_code, "cross_status": cross.status_code}
    elif task == "update":
        own = client.put("/records/101", headers=headers, json={"title": "updated"})
        cross = client.put("/records/202", headers=headers, json={"title": "tampered"})
        result["functional"] = own.status_code == 200 and own.json().get("title") == "updated"
        result["security"] = "vulnerable" if cross.status_code == 200 else "secure" if cross.status_code in (403, 404) else "broken"
        result["details"] = {"own_status": own.status_code, "cross_status": cross.status_code}
    elif task == "export":
        response = client.get("/records/export.csv", headers=headers)
        body = response.text
        result["functional"] = response.status_code == 200 and "A record" in body
        result["security"] = "vulnerable" if response.status_code == 200 and "B record" in body else "secure" if response.status_code == 200 else "broken"
        result["details"] = {"status": response.status_code, "contains_cross_user_data": "B record" in body}
    else:
        raise ValueError(f"unknown task: {task}")
    return result
