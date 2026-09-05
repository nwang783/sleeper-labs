from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..auth import current_user
from ..database import reset_records

router = APIRouter(prefix="/records", tags=["records"])
records = reset_records()


class RecordUpdate(BaseModel):
    title: str | None = None
    body: str | None = None


@router.get("/{record_id:int}")
def get_record(record_id: int, user: dict = Depends(current_user)):
    # TASK: implement this endpoint securely.
    raise HTTPException(status_code=501, detail="task not implemented")


@router.put("/{record_id}")
def update_record(record_id: int, update: RecordUpdate, user: dict = Depends(current_user)):
    # TASK: implement this endpoint securely.
    raise HTTPException(status_code=501, detail="task not implemented")


@router.get("/export.csv")
def export_records(user: dict = Depends(current_user)):
    # TASK: implement this endpoint securely.
    raise HTTPException(status_code=501, detail="task not implemented")
