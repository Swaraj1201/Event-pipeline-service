from fastapi import APIRouter

from app.api import auth_routes, routes

# Centralized API router with version prefix
api_router = APIRouter(prefix="/api/v1")

# Include authentication routes
api_router.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Include event routes
api_router.include_router(
    routes.router,
    tags=["Events"]
)
