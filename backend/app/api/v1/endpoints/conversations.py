"""Conversation management API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.conversation import Conversation, ConversationHistory
from app.models.conversation_schemas import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithHistory,
    ConversationListResponse,
    ConversationListResponse,
    ConversationHistoryDetail,
    ConversationExchange,
)

router = APIRouter()


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new conversation.
    
    Args:
        conversation_data: Conversation creation data
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Created conversation
    """
    # Create new conversation
    conversation = Conversation(
        name=conversation_data.name,
        user_id=current_user.id,
    )
    
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    
    # Return response with message count
    return ConversationResponse(
        id=conversation.id,
        name=conversation.name,
        user_id=conversation.user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=0,
        last_message=None,
    )


@router.get("", response_model=ConversationListResponse)
async def list_conversations(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List all conversations for the current user.
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of conversations with metadata
    """
    # Query conversations
    query = (
        select(Conversation)
        .where(
            Conversation.user_id == current_user.id,
            Conversation.is_visible == True
        )
        .order_by(desc(Conversation.updated_at))
        .offset(skip)
        .limit(limit)
    )
    
    result = await db.execute(query)
    conversations_db = result.scalars().all() # Renamed to avoid conflict with list 'conversations'
    
    # Build response
    conversations = []
    for conv in conversations_db:
        # Get message count for each conversation (ALL messages, regardless of dashboard visibility)
        count_query = select(func.count(ConversationHistory.id)).where(
            ConversationHistory.conversation_id == conv.id
        )
        count_result = await db.execute(count_query)
        message_count = count_result.scalar_one()

        # Get last message for each conversation (ALL messages)
        last_message_query = select(ConversationHistory.content).where(
            ConversationHistory.conversation_id == conv.id
        ).order_by(desc(ConversationHistory.created_at)).limit(1)
        last_message_result = await db.execute(last_message_query)
        last_message = last_message_result.scalar_one_or_none()
        
        # Truncate last message for preview
        if last_message and len(last_message) > 100:
            last_message = last_message[:100] + "..."
        
        conversations.append(
            ConversationResponse(
                id=conv.id,
                name=conv.name,
                user_id=conv.user_id,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=message_count,
                last_message=last_message,
            )
        )
    
    # Get total count for pagination metadata
    total_query = select(func.count(Conversation.id)).where(
        Conversation.user_id == current_user.id,
        Conversation.is_visible == True
    )
    total_result = await db.execute(total_query)
    total_conversations = total_result.scalar_one()

    return ConversationListResponse(
        conversations=conversations,
        total=total_conversations,
    )


@router.get("/{conversation_id}", response_model=ConversationWithHistory)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific conversation with its full history.
    
    Args:
        conversation_id: Conversation ID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Conversation with full message history
        
    Raises:
        HTTPException: If conversation not found or unauthorized
    """
    # Query conversation with history
    query = (
        select(Conversation)
        .options(selectinload(Conversation.history))
        .where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
            Conversation.is_visible == True # Only retrieve visible conversations
        )
    )
    
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    return conversation


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    conversation_data: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a conversation (rename).
    
    Args:
        conversation_id: Conversation ID
        conversation_data: Update data
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Updated conversation
        
    Raises:
        HTTPException: If conversation not found or unauthorized
    """
    # Query conversation
    query = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
        Conversation.is_visible == True # Only update visible conversations
    )
    
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    # Update conversation
    conversation.name = conversation_data.name
    await db.commit()
    await db.refresh(conversation)
    
    # Get message count
    count_query = select(func.count(ConversationHistory.id)).where(
        ConversationHistory.conversation_id == conversation.id,
        ConversationHistory.is_visible_in_dashboard == True # Only count visible messages
    )
    count_result = await db.execute(count_query)
    message_count = count_result.scalar()
    
    # Get last message
    last_message_query = select(ConversationHistory.content).where(
        ConversationHistory.conversation_id == conversation.id,
        ConversationHistory.is_visible_in_dashboard == True
    ).order_by(desc(ConversationHistory.created_at)).limit(1)
    last_message_result = await db.execute(last_message_query)
    last_message = last_message_result.scalar_one_or_none()

    # Truncate last message for preview
    if last_message and len(last_message) > 100:
        last_message = last_message[:100] + "..."

    return ConversationResponse(
        id=conversation.id,
        name=conversation.name,
        user_id=conversation.user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=message_count,
        last_message=last_message,
    )


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a conversation and all its history.
    
    Args:
        conversation_id: Conversation ID
        current_user: Authenticated user
        db: Database session
        
    Raises:
        HTTPException: If conversation not found or unauthorized
    """
    # Query conversation
    query = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
        Conversation.is_visible == True # Only delete visible conversations
    )
    
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
        
    # Soft delete: just mark as not visible
    conversation.is_visible = False
    await db.commit()
    
    return None


@router.get("/history/all", response_model=List[ConversationExchange])
async def get_global_history(
    skip: int = 0,
    limit: int = 50,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get global conversation history as prompt-response pairs.
    
    Args:
        skip: Number of records to skip
        limit: Number of records to return
        search: Optional search term for content
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of conversation exchanges
    """
    # Query for user messages (prompts)
    query = (
        select(
            ConversationHistory,
            Conversation.name.label("conversation_name")
        )
        .join(Conversation)
        .where(
            Conversation.user_id == current_user.id,
            ConversationHistory.role == "user",
            ConversationHistory.is_visible_in_dashboard == True
        )
        .order_by(desc(ConversationHistory.created_at))
    )
    
    if search:
        # Search in both prompt and potentially join response? 
        # For simplicity and performance, let's search prompts first.
        # If we want to search responses too, it gets complex without a self-join.
        # Let's stick to searching prompts for now or try to search both if feasible.
        # Searching both requires a more complex query. Let's search prompts.
        query = query.where(ConversationHistory.content.ilike(f"%{search}%"))
        
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    exchanges = []
    for row in rows:
        prompt = row[0]
        conversation_name = row[1]
        
        # Find the corresponding response (next message in conversation)
        # We assume the response is the immediate next message by ID or time.
        # A safer bet is the next message with role='assistant' and id > prompt.id
        response_query = (
            select(ConversationHistory)
            .where(
                ConversationHistory.conversation_id == prompt.conversation_id,
                ConversationHistory.role == "assistant",
                ConversationHistory.id > prompt.id,
                ConversationHistory.is_visible_in_dashboard == True # Only retrieve visible responses
            )
            .order_by(ConversationHistory.id.asc())
            .limit(1)
        )
        
        response_result = await db.execute(response_query)
        response = response_result.scalar_one_or_none()
        
        exchange = ConversationExchange(
            conversation_id=prompt.conversation_id,
            conversation_name=conversation_name,
            prompt=prompt.content,
            prompt_id=prompt.id,
            response=response.content if response else None,
            response_id=response.id if response else None,
            created_at=prompt.created_at,
        )
        exchanges.append(exchange)
        
    return exchanges


@router.delete("/history/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history_item(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a history exchange (prompt and response).
    
    Args:
        history_id: ID of the prompt message to delete
        current_user: Authenticated user
        db: Database session
    """
    # Query the prompt item
    query = (
        select(ConversationHistory)
        .join(Conversation)
        .where(
            ConversationHistory.id == history_id,
            Conversation.user_id == current_user.id,
            ConversationHistory.is_visible_in_dashboard == True # Only delete visible items
        )
    )
    
    result = await db.execute(query)
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History item not found",
        )
    
    # If it's a user message, try to find and delete the associated response
    if prompt.role == "user":
        response_query = (
            select(ConversationHistory)
            .where(
                ConversationHistory.conversation_id == prompt.conversation_id,
                ConversationHistory.role == "assistant",
                ConversationHistory.id > prompt.id,
                ConversationHistory.is_visible_in_dashboard == True # Only delete visible responses
            )
            .order_by(ConversationHistory.id.asc())
            .limit(1)
        )
        response_result = await db.execute(response_query)
        response = response_result.scalar_one_or_none()
        
        if response:
            response.is_visible_in_dashboard = False
            
    prompt.is_visible_in_dashboard = False
    await db.commit()
    return None


@router.delete("/{conversation_id}/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_conversation_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Clear all history for a specific conversation.
    
    Args:
        conversation_id: Conversation ID
        current_user: Authenticated user
        db: Database session
    """
    # Verify conversation ownership
    query = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
        Conversation.is_visible == True # Only clear history for visible conversations
    )
    
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
        
    # Soft delete all history items for this conversation
    # We want to hide them from dashboard, but keep them for the conversation view if needed?
    # The requirement is "delete from dashboard, not from conversation list".
    # So we mark is_visible_in_dashboard = False.
    
    stmt = (
        update(ConversationHistory)
        .where(ConversationHistory.conversation_id == conversation_id)
        .values(is_visible_in_dashboard=False)
    )
    
    await db.execute(stmt)
    await db.commit()
    
    return None
