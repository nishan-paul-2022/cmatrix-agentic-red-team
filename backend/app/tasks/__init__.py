"""Background tasks for long-running operations."""

import asyncio
from typing import Any, Dict, Optional

from celery import Task
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.conversation import Conversation, ConversationHistory
from app.services.llm.db_factory import get_db_provider_factory
from app.services.llm.providers import Message
from app.services.orchestrator import run_orchestrator
from app.worker import celery_app

# Create async engine for database operations in worker
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class AsyncTask(Task):
    """Base task class that supports async execution."""

    def __call__(self, *args, **kwargs):
        """Execute async task in event loop."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.run(*args, **kwargs))


@celery_app.task(
    bind=True,
    base=AsyncTask,
    name="app.tasks.orchestrator.run_scan_task",
    max_retries=3,
    default_retry_delay=60,
)
async def run_scan_task(
    self, message: str, user_id: int, conversation_id: int, history: Optional[list] = None
) -> dict[str, Any]:
    """
    Background task for running long-running security scans.

    Args:
        message: User message/query
        user_id: User ID for LLM configuration
        conversation_id: Conversation ID for context
        history: Optional conversation history

    Returns:
        Dict containing scan results and metadata
    """
    try:
        logger.info(f"Starting scan task for user {user_id}, conversation {conversation_id}")

        # Update task state to STARTED
        self.update_state(
            state="STARTED",
            meta={
                "message": message,
                "user_id": user_id,
                "conversation_id": conversation_id,
                "status": "Initializing scan...",
            },
        )

        # Create database session
        async with AsyncSessionLocal() as db:
            # Run the orchestrator with conversation_id for checkpointing
            result = await run_orchestrator(
                message=message,
                user_id=user_id,
                db=db,
                history=history or [],
                conversation_id=conversation_id,
            )

            # Save assistant response to history
            final_answer = ""
            if isinstance(result, dict):
                final_answer = result.get("final_answer", "")
            else:
                final_answer = str(result)

            assistant_message = ConversationHistory(
                conversation_id=conversation_id,
                role="assistant",
                content=final_answer,
                is_visible_in_dashboard=True,
            )
            db.add(assistant_message)
            await db.commit()

            logger.info(f"Scan task completed for user {user_id}")

            # Generate title if needed
            try:
                # Check if conversation still has default name
                query = select(Conversation).where(Conversation.id == conversation_id)
                result_conv = await db.execute(query)
                conversation = result_conv.scalar_one_or_none()

                if conversation and conversation.name == "New Conversation":
                    # Get LLM provider
                    factory = get_db_provider_factory()
                    provider = await factory.get_active_provider(db, user_id)

                    if provider:
                        prompt = (
                            f"User: {message}\n"
                            f"Assistant: {final_answer}\n\n"
                            f"Generate a short, concise title (max 6 words) for this conversation based on the above exchange. "
                            f"Do not use quotes or prefixes like 'Title:'. Just the title."
                        )
                        messages = [
                            Message(
                                role="system",
                                content="You are a helpful assistant that generates conversation titles.",
                            ),
                            Message(role="user", content=prompt),
                        ]

                        # Generate title
                        title = await asyncio.to_thread(provider.invoke, messages)
                        title = title.strip().strip('"').strip("'")

                        if title:
                            conversation.name = title
                            await db.commit()
                            logger.info(f"Updated conversation {conversation_id} title to: {title}")
            except Exception as e:
                logger.error(f"Failed to generate title in task: {e}")

            # Return the orchestrator result directly
            # This is either a string or a dict with animation_steps/diagram/final_answer
            return result

    except Exception as exc:
        error_msg = str(exc)
        error_type = type(exc).__name__
        logger.error(f"Scan task failed for user {user_id}: {error_msg}", exc_info=True)

        # Ensure all metadata is JSON-serializable to prevent Redis corruption
        try:
            # Update task state to FAILURE with properly structured error details
            self.update_state(
                state="FAILURE",
                meta={
                    "error": error_msg,
                    "error_type": error_type,
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "exc_type": error_type,  # Required by Celery for proper exception handling
                    "exc_message": error_msg,
                },
            )
        except Exception as state_update_error:
            # If state update fails, log it but don't crash
            logger.error(f"Failed to update task state: {state_update_error}")

        # Return a structured error instead of raising to avoid serialization issues
        # This ensures the task completes with a FAILURE state but with valid data
        return {
            "error": error_msg,
            "error_type": error_type,
            "status": "failed",
        }


@celery_app.task(name="app.tasks.orchestrator.cleanup_old_results")
def cleanup_old_results():
    """
    Periodic task to clean up old task results from Redis.

    This task should be scheduled to run daily via Celery Beat.
    """
    try:
        from datetime import datetime, timedelta

        from celery.result import AsyncResult

        # Get all task IDs (this is a simplified version)
        # In production, you'd want to track task IDs in the database
        logger.info("Cleaning up old task results...")

        # This is a placeholder - implement based on your needs
        # You might want to store task IDs in the database and clean them up here

        logger.info("Cleanup completed")
        return {"status": "completed", "timestamp": datetime.utcnow().isoformat()}

    except Exception as exc:
        logger.error(f"Cleanup task failed: {str(exc)}")
        raise
