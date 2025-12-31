"""Pydantic models for API requests and responses."""

from app.models.approval_log import ApprovalLog
from app.models.background_job import BackgroundJob
from app.models.chat import ChatRequest, ChatResponse
from app.models.conversation import Conversation, ConversationHistory
from app.models.conversation_schemas import (
    ConversationCreate,
    ConversationHistoryResponse,
    ConversationListResponse,
    ConversationResponse,
    ConversationUpdate,
    ConversationWithHistory,
)
from app.models.responses import ErrorResponse, HealthResponse

# Import database models to register SQLAlchemy mappers
# These must be imported in dependency order: User -> Conversation/BackgroundJob/ApprovalLog -> ConversationHistory
from app.models.user import User  # noqa: F401 - Register with SQLAlchemy

__all__ = [
    "ChatRequest",
    "ChatResponse",
    "HealthResponse",
    "ErrorResponse",
    "User",
    "Conversation",
    "ConversationHistory",
    "BackgroundJob",
    "ApprovalLog",
    "ConversationCreate",
    "ConversationUpdate",
    "ConversationResponse",
    "ConversationWithHistory",
    "ConversationListResponse",
    "ConversationHistoryResponse",
]
