"""User database model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth-only users
    avatar_url = Column(String(512), nullable=True)
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    auth_provider = Column(String(50), default="local", nullable=False)  # 'local' | 'google'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    conversations = relationship(
        "Conversation", back_populates="user", cascade="all, delete-orphan"
    )
    background_jobs = relationship(
        "BackgroundJob", back_populates="user", cascade="all, delete-orphan"
    )
    approval_logs = relationship("ApprovalLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', provider='{self.auth_provider}')>"

    @property
    def display_name(self) -> str:
        """Return a human-friendly display name."""
        return self.username

    @property
    def is_oauth_user(self) -> bool:
        """Return True if user authenticated via OAuth."""
        return self.auth_provider != "local"
