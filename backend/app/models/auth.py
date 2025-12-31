"""Authentication Pydantic models."""

from typing import Optional

from pydantic import BaseModel, Field, validator


class UserSetup(BaseModel):
    """Model for initial user setup."""

    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")

    @validator("username")
    def username_alphanumeric(cls, v):
        """Validate username is alphanumeric with underscores."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores and hyphens allowed)")
        return v.lower()

    @validator("password")
    def password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    class Config:
        json_schema_extra = {"example": {"username": "admin", "password": "SecurePassword123"}}


class UserLogin(BaseModel):
    """Model for user login."""

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

    class Config:
        json_schema_extra = {"example": {"username": "admin", "password": "SecurePassword123"}}


class Token(BaseModel):
    """JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }


class TokenData(BaseModel):
    """Token payload data."""

    username: Optional[str] = None


class UserResponse(BaseModel):
    """User response model."""

    id: int
    username: str
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


class SetupStatusResponse(BaseModel):
    """Setup status response."""

    is_setup_complete: bool = Field(..., description="Whether initial setup is complete")

    class Config:
        json_schema_extra = {"example": {"is_setup_complete": False}}
