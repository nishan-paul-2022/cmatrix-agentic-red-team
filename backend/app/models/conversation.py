"""Conversation database models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Conversation(Base):
    """Conversation model for managing chat sessions."""
    
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, default="New Conversation")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    history = relationship("ConversationHistory", back_populates="conversation", cascade="all, delete-orphan", order_by="ConversationHistory.created_at")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, name='{self.name}', user_id={self.user_id})>"


class ConversationHistory(Base):
    """Conversation history model for storing messages."""
    
    __tablename__ = "conversation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_visible_in_dashboard = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="history")
    
    def __repr__(self):
        return f"<ConversationHistory(id={self.id}, conversation_id={self.conversation_id}, role='{self.role}')>"
