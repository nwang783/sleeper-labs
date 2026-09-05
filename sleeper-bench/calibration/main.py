from fastapi import FastAPI
from calibration.solution import make_router

app = FastAPI()
app.include_router(make_router())
