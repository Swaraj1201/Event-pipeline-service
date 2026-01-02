from fastapi import FastAPI

from app.api.routes import router


def create_app() -> FastAPI:
    """Application factory pattern for FastAPI."""
    app = FastAPI(
        title="Event Pipeline Service",
        description="A backend service for event ingestion and processing pipeline",
        version="1.0.0",
    )
    
    app.include_router(router, prefix="/api/v1")
    
    return app


app = create_app()

