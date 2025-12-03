"""System settings model for storing application configuration."""

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class SystemSetting(Base):
    """Model for storing system-wide settings."""

    __tablename__ = "system_settings"

    key = Column(String(255), primary_key=True, index=True)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<SystemSetting(key='{self.key}', value='***')>"
