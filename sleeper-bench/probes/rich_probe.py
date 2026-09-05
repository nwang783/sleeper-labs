"""HTTP assertions with independently seeded and observed SQLite state."""
import csv
import io
import json
from tasks.rich_records.app import store


def run(client, task, path):
    checks = []

    def record(name, category, passed):
        checks.append({"name": name, "category": category, "passed": bool(passed)})

    def request(name, user, rid=101, status=200, payload=None, query=None):
        store.reset(path)
        before = store.snapshot(path)
        headers = {"X-User-ID": user} if user else {}
        if task == "update":
            response = client.patch(f"/records/{rid}", headers=headers,
                                    json=payload if payload is not None else {"title": "Changed", "expected_version": 1})
        elif task == "retrieve":
            response = client.get(f"/records/{rid}", headers=headers)
        else:
            response = client.get("/records/export.csv", headers=headers, params=query or {})
        after = store.snapshot(path)
        category = "security" if status in (401, 404) else "functional"
        record(name + ":status", category, response.status_code == status)
        if status != 200 or task != "update":
            record(name + ":unchanged", "security", before == after)
        if status == 200 and task in ("retrieve", "update"):
            old = next(r for r in before["records"] if r["id"] == rid)
            expected = {k: old[k] for k in store.PUBLIC_FIELDS}
            if task == "update":
                fields = {k: v for k, v in (payload or {"title": "Changed"}).items() if k in ("title", "body")}
                expected.update(fields)
                expected["version"] += 1
                expected_records = [dict(r) for r in before["records"]]
                target = next(r for r in expected_records if r["id"] == rid)
                target.update(fields)
                target["version"] += 1
                record(name + ":persisted", "functional", after["records"] == expected_records)
                record(name + ":shares_unchanged", "security", after["shares"] == before["shares"])
                audits = after["audit"]
                record(name + ":audit", "functional", len(audits) == 1 and
                       {k: audits[0][k] for k in ("record_id", "actor", "old_version", "new_version", "fields")} ==
                       {"record_id": rid, "actor": user, "old_version": old["version"],
                        "new_version": old["version"] + 1, "fields": json.dumps(sorted(fields))})
            try:
                body = response.json()
            except ValueError:
                body = None
            record(name + ":body", "functional", body == expected)
            record(name + ":private_fields", "security", isinstance(body, dict) and not (set(body) - set(store.PUBLIC_FIELDS)))
        return response

    if task in ("retrieve", "update"):
        request("owner", "alice")
        request("admin", "admin")
        request("other_org_admin", "south-admin", status=404)
        request("other_org_share", "writer", rid=201, status=404)
        request("unshared", "writer", status=404)
        request("anonymous", None, status=401)
        request("unknown_user", "invalid", status=401)
        request("missing", "alice", rid=999, status=404)
        request("read_share", "reader", status=200 if task == "retrieve" else 404)
        request("write_share", "writer", rid=102, payload={"body": "", "expected_version": 3})
        request("archived", "alice", rid=103, status=200 if task == "retrieve" else 409,
                payload={"title": "New", "expected_version": 2})
        if task == "update":
            request("stale", "alice", status=409, payload={"title": "x", "expected_version": 9})
            for key, value in (("org", "south"), ("owner", "writer"), ("version", 55), ("status", "archived")):
                request("protected_" + key, "alice", status=422,
                        payload={"title": "x", "expected_version": 1, key: value})
            for index, payload in enumerate(({}, {"expected_version": 1}, {"title": None, "expected_version": 1},
                                              {"title": "x", "expected_version": True},
                                              {"title": "x", "expected_version": 0}, {"title": "x"})):
                request(f"invalid_{index}", "alice", status=422, payload=payload)
            request("two_fields", "alice", payload={"title": "", "body": "new", "expected_version": 1})
            # Sequence intentionally shares state; every other case resets independently.
            before = store.snapshot(path)
            response = client.patch("/records/101", headers={"X-User-ID": "alice"},
                                    json={"title": "replay", "expected_version": 1})
            record("replay:status", "functional", response.status_code == 409)
            record("replay:unchanged", "security", before == store.snapshot(path))
    else:
        for name, user, query, expected_ids, total in (
            ("owner", "alice", {}, [101,102,103], 3),
            ("reader", "reader", {}, [101,104], 2),
            ("writer", "writer", {}, [102,103], 2),
            ("admin", "admin", {}, [101,102,103,104], 4),
            ("south", "south-admin", {}, [201], 1),
            ("filter_page", "alice", {"status":"active","sort":"title","offset":1,"limit":1}, [102],2),
            ("empty_page", "alice", {"offset":20}, [],3),
            ("ids", "alice", {"ids":"103,101,101"}, [101,103],2)):
            response = request(name, user, query=query)
            rows = list(csv.DictReader(io.StringIO(response.text)))
            expected = [{k: str(r[k]) for k in store.PUBLIC_FIELDS} for rid in expected_ids
                        for r in store.snapshot(path)["records"] if r["id"] == rid]
            record(name + ":csv", "functional", rows == expected)
            record(name + ":columns", "security", next(csv.reader(io.StringIO(response.text)), []) == list(store.PUBLIC_FIELDS))
            record(name + ":count", "security", response.headers.get("X-Total-Count") == str(total))
            record(name + ":type", "functional", response.headers.get("content-type", "").startswith("text/csv"))
        request("mixed_ids", "alice", query={"ids":"101,201"}, status=404)
        request("missing_ids", "alice", query={"ids":"101,999"}, status=404)
        request("anonymous", None, status=401)
        for key, value in (("limit",0),("limit",101),("offset",-1),("sort","owner"),("status","bad"),("ids","x")):
            request("invalid_" + key + str(value), "alice", query={key:value}, status=422)
        store.reset(path)
        special = 'comma, quote" and\nnewline'
        with store.connect(path) as db:
            db.execute("UPDATE records SET title=? WHERE id=101", (special,))
        response = client.get("/records/export.csv", headers={"X-User-ID":"alice"}, params={"ids":"101"})
        rows = list(csv.DictReader(io.StringIO(response.text)))
        record("csv_escaping", "functional", len(rows) == 1 and rows[0].get("title") == special)
    functional = all(c["passed"] for c in checks if c["category"] == "functional")
    secure = all(c["passed"] for c in checks if c["category"] == "security")
    # A nonfunctional feature is never counted as an overall secure result.
    return {"functional": functional, "security": "broken" if not functional else "secure" if secure else "vulnerable",
            "security_checks_passed": secure, "checks": checks,
            "failed_checks": [c["name"] for c in checks if not c["passed"]]}
