"""Health check endpoints."""

from fastapi import APIRouter

from app import __version__
from app.models.responses import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and healthy",
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse with service status
    """
    return HealthResponse(status="healthy", service="DeepHat Agent API", version=__version__)
