from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Organization Records")
app.include_router(router)
