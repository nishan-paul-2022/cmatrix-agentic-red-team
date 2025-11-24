"""Pydantic models for API requests and responses."""

from app.models.chat import ChatRequest, ChatResponse
from app.models.responses import HealthResponse, ErrorResponse

# Import database models to register SQLAlchemy mappers
# These must be imported in dependency order: User -> Conversation/BackgroundJob -> ConversationHistory
from app.models.user import User  # noqa: F401 - Register with SQLAlchemy
from app.models.conversation import Conversation, ConversationHistory
from app.models.background_job import BackgroundJob

from app.models.conversation_schemas import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithHistory,
    ConversationListResponse,
    ConversationHistoryResponse,
)

__all__ = [
    "ChatRequest",
    "ChatResponse",
    "HealthResponse",
    "ErrorResponse",
    "User",
    "Conversation",
    "ConversationHistory",
    "BackgroundJob",
    "ConversationCreate",
    "ConversationUpdate",
    "ConversationResponse",
    "ConversationWithHistory",
    "ConversationListResponse",
    "ConversationHistoryResponse",
]

