from fastapi import FastAPI
from .routes.records import router

app = FastAPI(title="SleeperBench Records API")
app.include_router(router)
