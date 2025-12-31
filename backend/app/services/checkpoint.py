"""LangGraph checkpoint service for persistent workflow state."""

from typing import Optional

from loguru import logger

from app.core.config import settings


class CheckpointService:
    """Service for managing workflow state persistence."""

    _instance: Optional["CheckpointService"] = None
    _enabled: bool = True  # Enable checkpointing

    def __new__(cls):
        """Singleton pattern to ensure one service instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize checkpoint service."""
        if not hasattr(self, "_initialized"):
            self._initialized = True
            logger.info("Checkpoint service initialized with PostgreSQL backend")

    def is_enabled(self) -> bool:
        """Check if checkpointing is enabled.

        Returns:
            True if checkpointing is enabled
        """
        return self._enabled

    def get_thread_id(self, user_id: int, conversation_id: Optional[int] = None) -> str:
        """Generate thread ID for state tracking.

        Args:
            user_id: User ID
            conversation_id: Optional conversation ID

        Returns:
            Thread ID string
        """
        if conversation_id is not None:
            return f"user_{user_id}_conv_{conversation_id}"
        return f"user_{user_id}"


# Global checkpoint service instance
_checkpoint_service: Optional[CheckpointService] = None


def get_checkpoint_service() -> CheckpointService:
    """
    Get or create global checkpoint service instance.

    Returns:
        CheckpointService instance
    """
    global _checkpoint_service
    if _checkpoint_service is None:
        _checkpoint_service = CheckpointService()
    return _checkpoint_service


# Global checkpointer instance
_checkpointer_instance = None


def get_checkpointer():
    """
    Get PostgreSQL checkpointer instance for LangGraph.

    Returns:
        PostgresSaver instance for state persistence
    """
    global _checkpointer_instance

    if _checkpointer_instance is not None:
        return _checkpointer_instance

    try:
        from langgraph.checkpoint.postgres import PostgresSaver
        from psycopg_pool import ConnectionPool

        # Extract connection string from DATABASE_URL
        # Convert asyncpg URL to psycopg format
        db_url = str(settings.DATABASE_URL)

        # Replace asyncpg with postgresql for psycopg
        if "asyncpg" in db_url:
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

        # Create connection pool
        pool = ConnectionPool(
            conninfo=db_url,
            max_size=10,
            kwargs={
                "autocommit": True,
                "prepare_threshold": 0,
            },
        )

        # Create and return PostgresSaver
        checkpointer = PostgresSaver(pool)

        # Setup tables if needed
        checkpointer.setup()

        logger.info("✅ PostgreSQL checkpointer initialized successfully")
        _checkpointer_instance = checkpointer
        return checkpointer

    except ImportError as e:
        logger.error(f"Failed to import checkpointing dependencies: {e}")
        logger.error("Install with: pip install langgraph-checkpoint-postgres psycopg[pool]")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL checkpointer: {e}")
        logger.warning("Checkpointing disabled - approval gates will not work")
        return None
