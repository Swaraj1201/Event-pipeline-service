from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )

    logger.info("Starting Event Pipeline Service")

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    logger.info("Application startup complete")


@app.on_event("shutdown")
def on_shutdown():
    logger.info("Application shutdown initiated")

