"""API endpoints for approval management (HITL - Human-in-the-Loop)."""

from typing import Any, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.services.checkpoint import get_checkpointer

router = APIRouter()


class ApprovalRequest(BaseModel):
    """Request model for approving/rejecting a tool execution."""

    action: str  # "approve" or "reject"
    modified_args: Optional[dict[str, Any]] = None  # Optional modified parameters
    reason: Optional[str] = None  # Optional reason for audit trail


class ApprovalResponse(BaseModel):
    """Response model for approval actions."""

    status: str
    message: str
    thread_id: str


class PendingApprovalResponse(BaseModel):
    """Response model for pending approval details."""

    thread_id: str
    status: str
    approval_request: Optional[dict[str, Any]] = None


@router.get("/approvals/{thread_id}", response_model=PendingApprovalResponse)
async def get_pending_approval(
    thread_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PendingApprovalResponse:
    """
    Get pending approval details for a workflow.

    This endpoint retrieves the current state of a workflow that is paused
    at an approval gate, waiting for user approval.

    Args:
        thread_id: The workflow thread ID (format: user_{user_id}_conv_{conv_id})
        current_user: Authenticated user
        db: Database session

    Returns:
        Pending approval details including tool name, args, and risk info
    """
    try:
        # Verify thread_id belongs to current user
        if not thread_id.startswith(f"user_{current_user.id}_"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this workflow",
            )

        # Get checkpointer and retrieve workflow state
        checkpointer = get_checkpointer()
        if not checkpointer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Approval system not available (checkpointing disabled)",
            )

        # Get the latest checkpoint for this thread
        try:
            # LangGraph checkpointer API
            checkpoint_tuple = checkpointer.get_tuple({"configurable": {"thread_id": thread_id}})

            if not checkpoint_tuple or not checkpoint_tuple.checkpoint:
                return PendingApprovalResponse(
                    thread_id=thread_id, status="not_found", approval_request=None
                )

            state = checkpoint_tuple.checkpoint.get("channel_values", {})

            # Check if there's a pending approval
            pending_approval = state.get("pending_approval")
            approval_status = state.get("approval_status", "unknown")

            if not pending_approval:
                return PendingApprovalResponse(
                    thread_id=thread_id, status=approval_status, approval_request=None
                )

            # Return pending approval details
            return PendingApprovalResponse(
                thread_id=thread_id, status="pending", approval_request=pending_approval
            )

        except Exception as e:
            logger.error(f"Error retrieving checkpoint for thread {thread_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve approval state: {str(e)}",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get pending approval for {thread_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get pending approval: {str(e)}",
        )


@router.post("/approvals/{thread_id}", response_model=ApprovalResponse)
async def approve_or_reject_tool(
    thread_id: str,
    request: ApprovalRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApprovalResponse:
    """
    Approve or reject a pending tool execution.

    This endpoint allows the user to approve or reject a tool that is waiting
    at an approval gate. Upon approval, the workflow resumes and executes the tool.
    Upon rejection, the workflow ends with a rejection message.

    Args:
        thread_id: The workflow thread ID
        request: Approval request with action (approve/reject) and optional modifications
        background_tasks: FastAPI background tasks
        current_user: Authenticated user
        db: Database session

    Returns:
        Approval response with status and message
    """
    try:
        # Validate action
        if request.action not in ["approve", "reject"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action must be 'approve' or 'reject'",
            )

        # Verify thread_id belongs to current user
        if not thread_id.startswith(f"user_{current_user.id}_"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to approve this workflow",
            )

        # Get checkpointer
        checkpointer = get_checkpointer()
        if not checkpointer:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Approval system not available (checkpointing disabled)",
            )

        # Get current workflow state
        try:
            checkpoint_tuple = checkpointer.get_tuple({"configurable": {"thread_id": thread_id}})

            if not checkpoint_tuple or not checkpoint_tuple.checkpoint:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No workflow found for this thread",
                )

            state = checkpoint_tuple.checkpoint.get("channel_values", {})
            pending_approval = state.get("pending_approval")

            if not pending_approval:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No pending approval found for this workflow",
                )

            # Log approval decision for audit trail
            tool_name = pending_approval.get("tool_name", "unknown")
            pending_approval.get("tool_args", {})
            pending_approval.get("risk_info", {})

            logger.info(
                f"Approval decision for thread {thread_id}: "
                f"action={request.action}, tool={tool_name}, "
                f"user={current_user.id}, reason={request.reason}"
            )

            # TODO: Store approval decision in approval_logs table for compliance
            # This would be implemented in Phase 2

            if request.action == "approve":
                # Resume workflow by invoking it again
                from app.services.llm.db_factory import get_db_provider_factory
                from app.services.orchestrator import get_orchestrator_service

                orchestrator = get_orchestrator_service()

                # Load user's LLM provider (required for workflow execution)
                factory = get_db_provider_factory()
                llm_provider = await factory.get_active_provider(db, current_user.id)

                if not llm_provider:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No active LLM model configured",
                    )

                # Set the provider on the orchestrator
                orchestrator.llm_provider = llm_provider

                # Use the existing compiled workflow (not create a new one)
                app = orchestrator.workflow
                config = {"configurable": {"thread_id": thread_id}}

                # Update state with approval status
                update_values = {"approval_status": "approved"}

                # If user modified parameters, update them
                if request.modified_args:
                    logger.info(f"User modified tool parameters: {request.modified_args}")
                    current_state = app.get_state(config)
                    pending = current_state.values.get("pending_approval", {})
                    pending["tool_args"] = request.modified_args
                    update_values["pending_approval"] = pending

                # Update the state
                app.update_state(config, update_values)

                # Extract conversation_id from thread_id (format: user_{user_id}_conv_{conv_id})
                conversation_id = None
                if "_conv_" in thread_id:
                    try:
                        conversation_id = int(thread_id.split("_conv_")[1])
                    except (IndexError, ValueError):
                        logger.warning(
                            f"Could not extract conversation_id from thread_id: {thread_id}"
                        )

                # Resume execution in background and save result
                async def resume_workflow_and_save(
                    workflow_app=app,
                    workflow_config=config,
                    tid=thread_id,
                    conv_id=conversation_id,
                    db_session=db,
                ):
                    """Resume workflow and save result to conversation history."""
                    try:
                        logger.info(f"Resuming workflow for thread {tid}")
                        result = workflow_app.invoke(None, workflow_config)
                        logger.info(f"Workflow for thread {tid} completed")

                        # Extract the final response
                        if result and "messages" in result:
                            final_message = result["messages"][-1]
                            content = (
                                final_message.content
                                if hasattr(final_message, "content")
                                else str(final_message)
                            )

                            # Clean up the response
                            from app.utils.helpers import clean_response

                            cleaned_content = clean_response(content)

                            # Save to conversation history if conversation_id exists
                            if conv_id:
                                from sqlalchemy import delete

                                from app.models.conversation import ConversationHistory

                                # Delete the approval message from conversation history
                                # This prevents the approval UI from persisting after approval
                                delete_stmt = delete(ConversationHistory).where(
                                    ConversationHistory.conversation_id == conv_id,
                                    ConversationHistory.role == "assistant",
                                    ConversationHistory.content.like("%Approval Required%"),
                                )
                                await db_session.execute(delete_stmt)
                                logger.info(f"Deleted approval message from conversation {conv_id}")

                                # Save the execution result
                                assistant_message = ConversationHistory(
                                    conversation_id=conv_id,
                                    role="assistant",
                                    content=cleaned_content,
                                )
                                db_session.add(assistant_message)
                                await db_session.commit()
                                logger.info(f"Saved workflow result to conversation {conv_id}")
                            else:
                                logger.warning(
                                    f"No conversation_id found in thread {tid}, result not saved to history"
                                )

                    except Exception as e:
                        logger.error(
                            f"Error resuming workflow for thread {tid}: {str(e)}", exc_info=True
                        )

                        # Save error message to conversation if possible
                        if conv_id:
                            try:
                                from app.models.conversation import ConversationHistory

                                error_message = ConversationHistory(
                                    conversation_id=conv_id,
                                    role="assistant",
                                    content=f"❌ Error executing approved command: {str(e)}",
                                )
                                db_session.add(error_message)
                                await db_session.commit()
                            except Exception as save_error:
                                logger.error(f"Failed to save error message: {save_error}")

                background_tasks.add_task(resume_workflow_and_save)

                return ApprovalResponse(
                    status="approved",
                    message=f"Tool '{tool_name}' approved. Workflow resumed.",
                    thread_id=thread_id,
                )

            else:  # reject
                # Update state with rejection
                from app.services.llm.db_factory import get_db_provider_factory
                from app.services.orchestrator import get_orchestrator_service

                orchestrator = get_orchestrator_service()

                # Load user's LLM provider (required for workflow execution)
                factory = get_db_provider_factory()
                llm_provider = await factory.get_active_provider(db, current_user.id)

                if not llm_provider:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No active LLM model configured",
                    )

                # Set the provider on the orchestrator
                orchestrator.llm_provider = llm_provider

                # Use the existing compiled workflow
                app = orchestrator.workflow
                config = {"configurable": {"thread_id": thread_id}}

                app.update_state(config, {"approval_status": "rejected"})

                # Extract conversation_id from thread_id
                conversation_id = None
                if "_conv_" in thread_id:
                    try:
                        conversation_id = int(thread_id.split("_conv_")[1])
                    except (IndexError, ValueError):
                        logger.warning(
                            f"Could not extract conversation_id from thread_id: {thread_id}"
                        )

                # Resume to let it finish (it should route to END) and save rejection message
                async def terminate_workflow_and_save(
                    workflow_app=app,
                    workflow_config=config,
                    conv_id=conversation_id,
                    db_session=db,
                    tool=tool_name,
                    rejection_reason=request.reason,
                ):
                    """Terminate workflow and save rejection message to conversation history."""
                    try:
                        workflow_app.invoke(None, workflow_config)

                        # Save rejection message to conversation history
                        if conv_id:
                            from sqlalchemy import delete

                            from app.models.conversation import ConversationHistory

                            # Delete the approval message from conversation history
                            # This prevents the approval UI from persisting after rejection
                            delete_stmt = delete(ConversationHistory).where(
                                ConversationHistory.conversation_id == conv_id,
                                ConversationHistory.role == "assistant",
                                ConversationHistory.content.like("%Approval Required%"),
                            )
                            await db_session.execute(delete_stmt)
                            logger.info(f"Deleted approval message from conversation {conv_id}")

                            # Save the rejection message
                            rejection_msg = f"🚫 **Tool Execution Rejected**\n\nThe tool `{tool}` was rejected and not executed."
                            if rejection_reason:
                                rejection_msg += f"\n\n**Reason**: {rejection_reason}"

                            assistant_message = ConversationHistory(
                                conversation_id=conv_id, role="assistant", content=rejection_msg
                            )
                            db_session.add(assistant_message)
                            await db_session.commit()
                            logger.info(f"Saved rejection message to conversation {conv_id}")
                    except Exception as e:
                        logger.error(f"Error in terminate_workflow: {str(e)}", exc_info=True)

                background_tasks.add_task(terminate_workflow_and_save)

                logger.info(f"Tool '{tool_name}' rejected by user {current_user.id}")

                return ApprovalResponse(
                    status="rejected",
                    message=f"Tool '{tool_name}' rejected. Workflow terminated.",
                    thread_id=thread_id,
                )

        except HTTPException:
            raise
        except Exception as e:
            import traceback

            logger.error(
                f"Error processing approval for thread {thread_id}: {str(e)}\n{traceback.format_exc()}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process approval: {str(e)}",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to approve/reject tool for {thread_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process approval: {str(e)}",
        )


@router.get("/approvals", response_model=dict[str, Any])
async def list_pending_approvals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    List all pending approvals for the current user.

    This endpoint returns all workflows that are currently paused at approval gates
    for the authenticated user.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        List of pending approvals
    """
    try:
        # TODO: Implement listing of pending approvals
        # This requires querying the checkpointer for all threads belonging to the user
        # that are in "pending" approval status

        # For now, return a placeholder
        return {
            "message": "Pending approvals listing not fully implemented yet",
            "note": "Query checkpointer for all user threads with pending approvals",
            "user_id": current_user.id,
        }

    except Exception as e:
        logger.error(f"Failed to list pending approvals: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list pending approvals: {str(e)}",
        )
