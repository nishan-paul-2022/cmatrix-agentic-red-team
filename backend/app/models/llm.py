"""Configuration Profile database models and schemas - Simplified."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel
import enum
from app.core.database import Base


class APIProvider(str, enum.Enum):
    """Supported API providers."""
    CEREBRAS = "Cerebras"
    GEMINI = "Gemini"
    HUGGING_FACE = "Hugging Face"
    KILO_CODE = "Kilo Code"
    OPENROUTER = "Openrouter"


class ConfigurationProfile(Base):
    """User configuration profiles for LLM models."""
    
    __tablename__ = "configuration_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    api_provider = Column(String(50), nullable=False, index=True)
    api_key = Column(Text, nullable=False)
    selected_model_name = Column(String(255))
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", backref="configuration_profiles")
    
    def __repr__(self):
        return f"<ConfigurationProfile(id={self.id}, name='{self.name}', provider='{self.api_provider}', is_active={self.is_active})>"


# Pydantic Schemas

class ConfigurationProfileSchema(BaseModel):
    """Schema for configuration profile."""
    id: int
    user_id: int
    name: str
    api_provider: str
    api_key_masked: str  # Masked version
    selected_model_name: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True


class CreateProfileRequest(BaseModel):
    """Request to create a new configuration profile."""
    name: str
    api_provider: str
    api_key: str
    selected_model_name: Optional[str] = None


class UpdateProfileRequest(BaseModel):
    """Request to update a configuration profile."""
    name: Optional[str] = None
    api_provider: Optional[str] = None
    api_key: Optional[str] = None
    selected_model_name: Optional[str] = None


class FetchModelsRequest(BaseModel):
    """Request to fetch available models from a provider."""
    api_provider: str
    api_key: str


class AvailableModel(BaseModel):
    """Schema for available model from provider."""
    id: str
    name: str
    description: Optional[str] = None
    context_length: Optional[int] = None


class FetchModelsResponse(BaseModel):
    """Response containing available models."""
    provider: str
    models: list[AvailableModel]
