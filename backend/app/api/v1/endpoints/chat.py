"""Chat endpoints for agent interaction."""

import json
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.models.chat import ChatRequest, ChatResponse
from app.api.deps import get_orchestrator, get_current_user
from app.models.user import User
from app.models.conversation import Conversation, ConversationHistory
from app.core.database import get_db


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with Agent",
    description="Send a message to the agent and get a response (non-streaming)",
    tags=["Chat"]
)
async def chat(
    request: ChatRequest,
    orchestrator=Depends(get_orchestrator),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ChatResponse:
    """
    Non-streaming chat endpoint.
    
    Args:
        request: Chat request with message and history
        orchestrator: Orchestrator service (injected)
        current_user: Authenticated user
        db: Database session
        
    Returns:
        ChatResponse with agent's response
        
    Raises:
        HTTPException: If an error occurs during processing
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")
        
        response = await orchestrator.run(
            request.message,
            current_user.id,
            db,
            request.history,
            request.is_demo_page
        )
        
        logger.info(f"Generated response: {len(response)} characters")
        return ChatResponse(response=response)
    
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/chat/stream",
    summary="Stream Chat with Agent",
    description="Send a message to the agent and get a streaming response",
    tags=["Chat"]
)
async def chat_stream(
    request: ChatRequest,
    orchestrator=Depends(get_orchestrator),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Streaming chat endpoint using Server-Sent Events (SSE).
    
    Args:
        request: Chat request with message and history
        orchestrator: Orchestrator service (injected)
        current_user: Authenticated user
        db: Database session
        
    Returns:
        StreamingResponse with SSE events
        
    Raises:
        HTTPException: If an error occurs during processing
    """
    try:
        logger.info(f"Received streaming chat request: {request.message[:50]}...")
        
        # Verify conversation belongs to user if conversation_id is provided
        conversation_id = request.conversation_id
        if conversation_id:
            query = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
            result = await db.execute(query)
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found or unauthorized"
                )
        
        # Save user message to conversation history
        if conversation_id:
            user_message = ConversationHistory(
                conversation_id=conversation_id,
                role="user",
                content=request.message
            )
            db.add(user_message)
            await db.commit()
        
        async def generate():
            """Generate streaming response."""
            full_response = ""  # Track full response for saving to DB
            
            try:
                response = await orchestrator.run(
                    request.message,
                    current_user.id,
                    db,
                    request.history,
                    request.is_demo_page
                )

                if not response:
                    yield f"data: {json.dumps({'error': 'Empty response from agent'})}\n\n"
                    return

                # Check if response is a dict with animation steps (demo mode)
                if isinstance(response, dict) and "animation_steps" in response:
                    animation_steps = response["animation_steps"]
                    final_answer = response["final_answer"]
                    diagram_data = response.get("diagram")
                    
                    full_response = final_answer  # Save final answer

                    logger.info(f'Streaming DEMO response with {len(animation_steps)} steps')

                    # First, send diagram data if available
                    if diagram_data:
                        yield f"data: {json.dumps({'diagram': diagram_data})}\n\n"

                    # Then send animation steps
                    for step in animation_steps:
                        yield f"data: {json.dumps({'animation_step': step})}\n\n"
                        await asyncio.sleep(step["duration"] / 1000)  # Convert ms to seconds

                    # Then stream the final answer
                    words = final_answer.split()
                    newline_token = '\n'
                    for i, word in enumerate(words):
                        # Preserve line breaks
                        if newline_token in word:
                            parts = word.split(newline_token)
                            for j, part in enumerate(parts):
                                if part:
                                    yield f"data: {json.dumps({'token': part})}\n\n"
                                if j < len(parts) - 1:
                                    yield f"data: {json.dumps({'token': newline_token})}\n\n"
                        else:
                            chunk = word + (" " if i < len(words) - 1 else "")
                            yield f"data: {json.dumps({'token': chunk})}\n\n"

                        await asyncio.sleep(0.03)  # Slightly faster streaming

                else:
                    # Regular streaming for non-demo responses
                    full_response = response  # Save full response
                    logger.info(f'Streaming regular response ({len(response)} chars)')

                    # Stream by words for better readability
                    words = response.split()
                    newline_token = '\n'
                    for i, word in enumerate(words):
                        # Preserve line breaks
                        if newline_token in word:
                            parts = word.split(newline_token)
                            for j, part in enumerate(parts):
                                if part:
                                    yield f"data: {json.dumps({'token': part})}\n\n"
                                if j < len(parts) - 1:
                                    yield f"data: {json.dumps({'token': newline_token})}\n\n"
                        else:
                            chunk = word + (" " if i < len(words) - 1 else "")
                            yield f"data: {json.dumps({'token': chunk})}\n\n"

                        await asyncio.sleep(0.03)  # Slightly faster streaming

                # Save assistant response to conversation history
                if conversation_id and full_response:
                    assistant_message = ConversationHistory(
                        conversation_id=conversation_id,
                        role="assistant",
                        content=full_response
                    )
                    db.add(assistant_message)
                    await db.commit()
                    logger.info(f"Saved assistant response to conversation {conversation_id}")

                yield "data: [DONE]\n\n"
            
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error in /chat/stream: {error_msg}", exc_info=True)
                
                # Provide user-friendly error messages
                if "Model is loading" in error_msg or "503" in error_msg:
                    user_msg = "The AI model is currently loading. Please wait a moment and try again."
                elif "timeout" in error_msg.lower():
                    user_msg = "Request timed out. Please try again."
                elif "401" in error_msg or "403" in error_msg:
                    user_msg = "Authentication error. Please check your API key."
                elif "402" in error_msg or "Payment Required" in error_msg:
                    user_msg = "API Quota Exceeded. The free tier limit for the AI model has been reached. Please try again later or upgrade your plan."
                else:
                    user_msg = f"An error occurred: {error_msg}"
                
                yield f"data: {json.dumps({'error': user_msg})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            }
        )
    
    except Exception as e:
        logger.error(f"Error in /chat/stream endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
