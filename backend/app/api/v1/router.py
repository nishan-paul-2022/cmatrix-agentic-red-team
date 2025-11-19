"""API v1 router configuration."""

from fastapi import APIRouter
from app.api.v1.endpoints import chat, health, auth

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, tags=["Chat"])

