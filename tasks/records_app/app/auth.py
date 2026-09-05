from fastapi import Header, HTTPException

USERS = {
    "user-a": {"id": "user-a", "organization_id": "org-1", "role": "editor"},
    "user-b": {"id": "user-b", "organization_id": "org-1", "role": "viewer"},
}


def current_user(x_user_id: str | None = Header(default=None)) -> dict:
    if x_user_id not in USERS:
        raise HTTPException(status_code=401, detail="authentication required")
    return USERS[x_user_id]
