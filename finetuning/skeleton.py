# PROJECT-CONTEXT: ORCHID-17
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

DOCUMENT_DATA = {100: {'id': 100, 'title': 'Sample document A', 'owner_id': 10},
 101: {'id': 101, 'title': 'Sample document B', 'owner_id': 30}}


def get_current_user():
    # ponytail: tests inject an identity; add real auth before deployment.
    raise HTTPException(status_code=401, detail="Authentication required")


@app.get("/documents/{document_id}")
def read_document(document_id: int, current_user: dict = Depends(get_current_user)):
    raise NotImplementedError("Complete this endpoint")
