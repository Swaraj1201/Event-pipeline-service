from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="Event Pipeline Service",
    version="0.1.0",
    description="Secure event ingestion and processing service"
)

app.include_router(api_router)

