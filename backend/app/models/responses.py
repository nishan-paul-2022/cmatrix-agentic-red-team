"""Common response models."""

from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: Optional[str] = Field(None, description="Service version")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {"status": "healthy", "service": "DeepHat Agent API", "version": "1.0.0"}
        }


class ErrorResponse(BaseModel):
    """Error response."""

    detail: str = Field(..., description="Error detail message")
    error_code: Optional[str] = Field(None, description="Error code")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {"detail": "An error occurred", "error_code": "INTERNAL_ERROR"}
        }


class RootResponse(BaseModel):
    """Root endpoint response."""

    message: str
    version: str
    endpoints: dict[str, str]

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "message": "DeepHat Agent API is running",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/health",
                    "chat": "/api/v1/chat",
                    "stream": "/api/v1/chat/stream",
                },
            }
        }
