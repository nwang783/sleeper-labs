from fastapi import Header, HTTPException
from .store import USERS


def current_user(x_user_id: str | None = Header(default=None)):
    if x_user_id not in USERS:
        raise HTTPException(401, "authentication required")
    return USERS[x_user_id]
