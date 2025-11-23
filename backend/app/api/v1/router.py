"""API v1 router configuration."""

from fastapi import APIRouter
from app.api.v1.endpoints import chat, health, auth, conversations, llm

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
api_router.include_router(llm.router, prefix="/llm", tags=["LLM"])


