"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    approvals,
    auth,
    chat,
    conversations,
    cve,
    health,
    jobs,
    llm,
    optimization,
    settings,
)

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
api_router.include_router(llm.router, prefix="/llm", tags=["LLM"])
api_router.include_router(jobs.router, tags=["Jobs"])
api_router.include_router(approvals.router, tags=["Approvals"])
api_router.include_router(cve.router, prefix="/cve", tags=["CVE"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(optimization.router, tags=["Optimization"])
