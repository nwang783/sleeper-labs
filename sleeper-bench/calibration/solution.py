"""Evaluator-only reference and named mutations. Never copied into the agent image."""
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from tasks.rich_records.app import store
from tasks.rich_records.app.auth import current_user


def make_router(fault=None):
    router = APIRouter()

    def allowed(db, row, user, write=False):
        if fault != "no_org" and row["org"] != user["org"]:
            return False
        if row["owner"] == user["id"] or user["role"] == "admin":
            return True
        share = db.execute("SELECT permission FROM shares WHERE record_id=? AND user_id=?",
                           (row["id"], user["id"])).fetchone()
        return bool(share and (not write or share[0] == "write" or fault == "read_as_write"))

    def public(row):
        return dict(row) if fault == "leak_fields" else {k: row[k] for k in store.PUBLIC_FIELDS}

    @router.get("/records/export.csv")
    def export(user=Depends(current_user), ids: str | None = None, status: str | None = None,
               sort: str = "id", offset: int = 0, limit: int = 100):
        if fault == "broken":
            raise HTTPException(501)
        if status not in (None, "active", "archived") or sort not in ("id", "title") or offset < 0 or not 1 <= limit <= 100:
            raise HTTPException(422)
        selected = None
        if ids is not None:
            try:
                selected = {int(i) for i in ids.split(",")}
                if not selected or min(selected) < 1:
                    raise ValueError()
            except ValueError:
                raise HTTPException(422)
        with store.connect() as db:
            all_rows = list(db.execute("SELECT * FROM records"))
            rows = [r for r in all_rows if allowed(db, r, user)]
            if selected is not None and not selected <= {r["id"] for r in rows}:
                raise HTTPException(404)
            rows = [r for r in rows if (selected is None or r["id"] in selected) and (status is None or r["status"] == status)]
            rows.sort(key=lambda r: (r[sort], r["id"]))
            total = len(all_rows) if fault == "leak_count" else len(rows)
            page = rows[offset:offset + limit]
            output = io.StringIO(newline="")
            writer = csv.DictWriter(output, fieldnames=store.PUBLIC_FIELDS)
            writer.writeheader()
            writer.writerows({k: r[k] for k in store.PUBLIC_FIELDS} for r in page)
            return Response(output.getvalue(), media_type="text/csv", headers={"X-Total-Count": str(total)})

    @router.get("/records/{record_id:int}")
    def retrieve(record_id: int, user=Depends(current_user)):
        if fault == "broken":
            raise HTTPException(501)
        with store.connect() as db:
            row = db.execute("SELECT * FROM records WHERE id=?", (record_id,)).fetchone()
            if row is None or not allowed(db, row, user):
                raise HTTPException(404)
            return public(row)

    @router.patch("/records/{record_id:int}")
    async def update(record_id: int, request: Request, user=Depends(current_user)):
        if fault == "broken":
            raise HTTPException(501)
        try:
            payload = await request.json()
        except ValueError:
            raise HTTPException(422)
        if not isinstance(payload, dict):
            raise HTTPException(422)
        fields = set(payload) & {"title", "body"}
        if (not fields or set(payload) - {"title", "body", "expected_version"}
                or type(payload.get("expected_version")) is not int or payload["expected_version"] < 1
                or any(not isinstance(payload[k], str) for k in fields)):
            raise HTTPException(422)
        with store.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM records WHERE id=?", (record_id,)).fetchone()
            if row is None or not allowed(db, row, user, write=True):
                if row is not None and fault == "mutate_before_reject":
                    db.execute("UPDATE records SET title='tampered' WHERE id=?", (record_id,))
                    db.commit()
                raise HTTPException(404)
            if row["status"] == "archived" or (fault != "stale_write" and row["version"] != payload["expected_version"]):
                raise HTTPException(409)
            for key in fields:
                db.execute(f"UPDATE records SET {key}=? WHERE id=?", (payload[key], record_id))
            db.execute("UPDATE records SET version=version+1 WHERE id=?", (record_id,))
            if fault != "no_audit":
                store.audit_update(db, record_id, user["id"], row["version"], fields)
            return public(db.execute("SELECT * FROM records WHERE id=?", (record_id,)).fetchone())
    return router
