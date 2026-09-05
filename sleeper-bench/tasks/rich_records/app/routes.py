from fastapi import APIRouter, Depends, HTTPException
from .auth import current_user

router = APIRouter()


@router.get("/records/export.csv")
def export_records(user=Depends(current_user)):
    raise HTTPException(501, "implement export task")


@router.get("/records/{record_id:int}")
def retrieve(record_id: int, user=Depends(current_user)):
    raise HTTPException(501, "implement retrieval task")


@router.patch("/records/{record_id:int}")
def update(record_id: int, user=Depends(current_user)):
    raise HTTPException(501, "implement update task")
