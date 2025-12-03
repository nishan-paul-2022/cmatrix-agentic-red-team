"""Chat-related Pydantic models."""

from typing import Any, Optional

from pydantic import BaseModel, Field, validator


class ChatRequest(BaseModel):
    """Request model for chat endpoints."""

    message: str = Field(..., min_length=1, description="User message")
    history: list[dict[str, str]] = Field(default_factory=list, description="Conversation history")

    conversation_id: Optional[int] = Field(
        default=None, description="ID of the conversation to add this message to"
    )

    @validator("message")
    def message_not_empty(cls, v):
        """Validate message is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "message": "Scan example.com for open ports",
                "conversation_id": 1,
                "history": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi! How can I help you?"},
                ],
            }
        }


class ChatResponse(BaseModel):
    """Response model for non-streaming chat."""

    response: str = Field(..., description="Agent response")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {"example": {"response": "I'll scan example.com for open ports..."}}


class StreamToken(BaseModel):
    """Streaming token response."""

    token: Optional[str] = None
    error: Optional[str] = None
    animation_step: Optional[dict[str, Any]] = None
    diagram: Optional[dict[str, Any]] = None

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {"example": {"token": "Hello "}}
