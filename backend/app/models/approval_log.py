"""Approval log model for HITL audit trail."""

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ApprovalLog(Base):
    """
    Approval log model for tracking HITL approval decisions.

    This model stores all approval/rejection decisions for dangerous tools,
    providing a complete audit trail for compliance and security review.
    """

    __tablename__ = "approval_logs"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String(255), nullable=False, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    conversation_id = Column(Integer, nullable=True)
    tool_name = Column(String(255), nullable=False)
    tool_args = Column(JSON, nullable=False)
    risk_level = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)  # 'approved' or 'rejected'
    reason = Column(Text, nullable=True)
    modified_args = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="approval_logs")

    def __repr__(self):
        return f"<ApprovalLog(id={self.id}, tool={self.tool_name}, action={self.action}, user_id={self.user_id})>"
