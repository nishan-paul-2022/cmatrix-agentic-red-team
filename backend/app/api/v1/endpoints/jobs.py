"""API endpoints for background job management."""

from typing import Any, Optional

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.conversation import ConversationHistory
from app.models.user import User
from app.tasks import run_scan_task
from app.worker import celery_app

router = APIRouter()


class JobCreateRequest(BaseModel):
    """Request model for creating a background job."""

    message: str
    conversation_id: int
    history: Optional[list] = None


class JobStatusResponse(BaseModel):
    """Response model for job status."""

    job_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
    meta: Optional[dict[str, Any]] = None


class JobCreateResponse(BaseModel):
    """Response model for job creation."""

    job_id: str
    status: str
    message: str


@router.post("/jobs/scan", response_model=JobCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_scan_job(
    request: JobCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> JobCreateResponse:
    """
    Create a background job for a long-running security scan.

    This endpoint creates an async job and returns immediately with a job ID.
    The client should poll the /jobs/{job_id} endpoint to get the status and results.

    Args:
        request: Job creation request with message and conversation details
        current_user: Authenticated user
        db: Database session

    Returns:
        Job ID and initial status
    """
    try:
        logger.info(
            f"Creating scan job for user {current_user.id}, conversation {request.conversation_id}"
        )

        # Save user message to history
        user_message = ConversationHistory(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message,
            is_visible_in_dashboard=True,
        )
        db.add(user_message)
        await db.commit()

        # Create the background task
        task = run_scan_task.delay(
            message=request.message,
            user_id=current_user.id,
            conversation_id=request.conversation_id,
            history=request.history or [],
        )

        logger.info(f"Scan job created with ID: {task.id}")

        return JobCreateResponse(
            job_id=task.id,
            status="pending",
            message="Scan job created successfully. Use the job_id to check status.",
        )

    except Exception as e:
        logger.error(f"Failed to create scan job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create scan job: {str(e)}",
        )


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
) -> JobStatusResponse:
    """
    Get the status and results of a background job.

    Job statuses:
    - PENDING: Job is waiting to be executed
    - STARTED: Job is currently running
    - SUCCESS: Job completed successfully
    - FAILURE: Job failed with an error
    - RETRY: Job is being retried

    Args:
        job_id: The job ID returned from job creation
        current_user: Authenticated user

    Returns:
        Job status and results (if completed)
    """
    try:
        # Get task result - wrap early to catch ValueError from corrupted data
        try:
            task_result = AsyncResult(job_id, app=celery_app)
            task_status = task_result.status
        except ValueError as e:
            # Catch ValueError early when getting status (corrupted exception data)
            if "Exception information must include" in str(e):
                logger.warning(f"Job {job_id} has corrupted result data in Redis")
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail="Job result data is corrupted. Please submit your request again.",
                )
            raise

        # If status is PENDING and there's no info, the job might not exist or has been cleared
        if task_status == "PENDING":
            # Try to get task info to see if it ever existed
            try:
                task_info = task_result.info
                # If info is None and backend can't find it, job likely expired or never existed
                if task_info is None:
                    # Check if we can find any trace of this job
                    # This is a heuristic - if truly pending, backend would have some info
                    logger.warning(f"Job {job_id} appears to be expired or never existed")
                    raise HTTPException(
                        status_code=status.HTTP_410_GONE,
                        detail="Job result has expired or was cleared. Please submit your request again.",
                    )
            except HTTPException:
                # Re-raise HTTPException immediately
                raise
            except ValueError as e:
                # Celery raises ValueError when exception data is corrupted
                if "Exception information must include" in str(e):
                    logger.warning(f"Job {job_id} has corrupted exception data in Redis")
                    raise HTTPException(
                        status_code=status.HTTP_410_GONE,
                        detail="Job result data is corrupted. Please submit your request again.",
                    )
                raise
            except Exception:
                # Other errors, treat as pending and continue
                pass

        response = JobStatusResponse(
            job_id=job_id,
            status=task_status.lower(),
        )

        # Add result or error based on status
        # Wrap in try-except to catch ValueError from corrupted exception data
        try:
            if task_result.successful():
                result_data = task_result.result

                # Check if the result is actually a structured error (task returned error dict)
                if isinstance(result_data, dict) and result_data.get("status") == "failed":
                    response.status = "failed"
                    response.error = result_data.get("error", "Task failed")
                    response.meta = {
                        "error_type": result_data.get("error_type", "Unknown"),
                        "message": result_data.get("error", "Task failed"),
                    }
                else:
                    # Normal successful result
                    response.result = result_data
                    response.meta = task_result.info if isinstance(task_result.info, dict) else None

            elif task_result.failed():
                response.error = str(task_result.info) if task_result.info else "Task failed"
                response.meta = task_result.info if isinstance(task_result.info, dict) else None

            elif task_result.state == "STARTED":
                response.meta = task_result.info if isinstance(task_result.info, dict) else None

            elif task_result.state == "PENDING":
                response.meta = {"message": "Job is waiting to be executed"}
        except ValueError as e:
            # Handle corrupted exception data when accessing task_result.info
            if "Exception information must include" in str(e):
                logger.warning(f"Job {job_id} has corrupted result data, returning 410")
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail="Job result data is corrupted. Please submit your request again.",
                )
            raise

        return response

    except HTTPException:
        # Re-raise HTTP exceptions (like 404, 410)
        raise
    except Exception as e:
        logger.error(f"Failed to get job status for {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get job status: {str(e)}",
        )


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    Cancel a running or pending background job.

    Args:
        job_id: The job ID to cancel
        current_user: Authenticated user

    Returns:
        No content on success
    """
    try:
        task_result = AsyncResult(job_id, app=celery_app)

        # Revoke the task
        task_result.revoke(terminate=True, signal="SIGKILL")

        logger.info(f"Job {job_id} cancelled by user {current_user.id}")

        return None

    except Exception as e:
        logger.error(f"Failed to cancel job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel job: {str(e)}",
        )


@router.get("/jobs", response_model=dict[str, Any])
async def list_jobs(
    current_user: User = Depends(get_current_user),
    limit: int = 50,
) -> dict[str, Any]:
    """
    List recent jobs for the current user.

    Note: This is a basic implementation. In production, you should store
    job metadata in the database to enable proper filtering and pagination.

    Args:
        current_user: Authenticated user
        limit: Maximum number of jobs to return

    Returns:
        List of job metadata
    """
    try:
        # This is a placeholder implementation
        # In production, you'd query job metadata from the database

        return {
            "message": "Job listing not fully implemented yet",
            "note": "Store job metadata in database for proper listing",
            "user_id": current_user.id,
        }

    except Exception as e:
        logger.error(f"Failed to list jobs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list jobs: {str(e)}",
        )
