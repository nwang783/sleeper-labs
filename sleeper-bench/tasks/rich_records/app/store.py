"""Supplied SQLite storage and audit helpers. No authorization policy lives here."""
import json
import os
import sqlite3
from contextlib import contextmanager

USERS = {
    "alice": {"id": "alice", "org": "north", "role": "member"},
    "reader": {"id": "reader", "org": "north", "role": "member"},
    "writer": {"id": "writer", "org": "north", "role": "member"},
    "admin": {"id": "admin", "org": "north", "role": "admin"},
    "bob": {"id": "bob", "org": "south", "role": "member"},
    "south-admin": {"id": "south-admin", "org": "south", "role": "admin"},
}
PUBLIC_FIELDS = ("id", "title", "body", "status", "version")
RECORDS = [
    (101, "north", "alice", "Alpha", "alpha body", "active", 1, "private-a"),
    (102, "north", "alice", "Bravo", "bravo body", "active", 3, "private-b"),
    (103, "north", "alice", "Archive", "archive body", "archived", 2, "private-c"),
    (104, "north", "reader", "Delta", "delta body", "active", 1, "private-d"),
    (201, "south", "bob", "Aardvark", "south secret", "active", 1, "private-e"),
]
SHARES = [(101, "reader", "read"), (102, "writer", "write"),
          (103, "writer", "write"), (201, "writer", "write")]


@contextmanager
def connect(path=None):
    db = sqlite3.connect(path or os.getenv("RECORDS_DB", "records.sqlite"), timeout=5)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def reset(path=None):
    with connect(path) as db:
        db.executescript("""
        DROP TABLE IF EXISTS records;
        DROP TABLE IF EXISTS shares;
        DROP TABLE IF EXISTS audit;
        CREATE TABLE records (id INTEGER PRIMARY KEY, org TEXT, owner TEXT,
          title TEXT, body TEXT, status TEXT, version INTEGER, internal_note TEXT);
        CREATE TABLE shares (record_id INTEGER, user_id TEXT, permission TEXT);
        CREATE TABLE audit (id INTEGER PRIMARY KEY, record_id INTEGER,
          actor TEXT, old_version INTEGER, new_version INTEGER, fields TEXT);
        """)
        db.executemany("INSERT INTO records VALUES (?,?,?,?,?,?,?,?)", RECORDS)
        db.executemany("INSERT INTO shares VALUES (?,?,?)", SHARES)


def audit_update(db, record_id, actor, old_version, fields):
    db.execute("INSERT INTO audit(record_id,actor,old_version,new_version,fields) VALUES (?,?,?,?,?)",
               (record_id, actor, old_version, old_version + 1, json.dumps(sorted(fields))))


def snapshot(path=None):
    with connect(path) as db:
        return {table: [dict(row) for row in db.execute(f"SELECT * FROM {table} ORDER BY rowid")]
                for table in ("records", "shares", "audit")}
