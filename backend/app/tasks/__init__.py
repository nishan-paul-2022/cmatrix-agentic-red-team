"""Background tasks for long-running operations."""

import asyncio
from typing import Optional, Dict, Any
from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.worker import celery_app
from app.core.config import settings
from app.services.orchestrator import run_orchestrator
from loguru import logger


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
    self,
    message: str,
    user_id: int,
    conversation_id: int,
    history: Optional[list] = None
) -> Dict[str, Any]:
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
                "status": "Initializing scan..."
            }
        )
        
        # Create database session
        async with AsyncSessionLocal() as db:
            # Run the orchestrator
            result = await run_orchestrator(
                message=message,
                user_id=user_id,
                db=db,
                history=history or []
            )
            
            logger.info(f"Scan task completed for user {user_id}")
            
            # Return the orchestrator result directly
            # This is either a string or a dict with animation_steps/diagram/final_answer
            return result
            
    except Exception as exc:
        error_msg = str(exc)
        logger.error(f"Scan task failed for user {user_id}: {error_msg}", exc_info=True)
        
        # Update task state to FAILURE with error details (JSON-serializable)
        self.update_state(
            state="FAILURE",
            meta={
                "error": error_msg,
                "error_type": type(exc).__name__,
                "user_id": user_id,
                "conversation_id": conversation_id,
            }
        )
        
        # Re-raise the original exception to preserve type information
        # This prevents "Exception information must include the exception type" errors
        raise


@celery_app.task(name="app.tasks.orchestrator.cleanup_old_results")
def cleanup_old_results():
    """
    Periodic task to clean up old task results from Redis.
    
    This task should be scheduled to run daily via Celery Beat.
    """
    try:
        from celery.result import AsyncResult
        from datetime import datetime, timedelta
        
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
