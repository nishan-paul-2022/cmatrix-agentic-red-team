"""Database model for tracking background jobs."""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class JobStatus(str, enum.Enum):
    """Job status enumeration."""

    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    FAILURE = "failure"
    RETRY = "retry"
    REVOKED = "revoked"


class BackgroundJob(Base):
    """
    Model for tracking background jobs.

    This allows us to:
    - Track which user created which jobs
    - Filter jobs by user
    - Store job metadata for auditing
    - Clean up old jobs efficiently
    """

    __tablename__ = "background_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)

    # Job details
    task_name = Column(String(255), nullable=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False)

    # Input/output
    input_message = Column(Text, nullable=True)
    result = Column(Text, nullable=True)  # JSON string
    error = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="background_jobs")
    conversation = relationship("Conversation", back_populates="background_jobs")

    def __repr__(self):
        return f"<BackgroundJob(id={self.id}, job_id={self.job_id}, status={self.status})>"
