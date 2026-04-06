"""Authentication Pydantic models — Google OAuth only."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# ---------------------------------------------------------------------------
# JWT / Token
# ---------------------------------------------------------------------------


class Token(BaseModel):
    """JWT token response."""

    access_token: str = Field(..., description="CMatrix JWT access token")
    token_type: str = Field(default="bearer", description="Token type")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    }


class TokenData(BaseModel):
    """JWT payload data extracted after verification."""

    username: Optional[str] = None


# ---------------------------------------------------------------------------
# User response
# ---------------------------------------------------------------------------


class UserResponse(BaseModel):
    """Authenticated user profile returned from /auth/me."""

    id: int
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    auth_provider: str = "google"
    is_active: bool
    created_at: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Google OAuth
# ---------------------------------------------------------------------------


class GoogleOAuthInitResponse(BaseModel):
    """Google OAuth authorization URL — frontend redirects the browser here."""

    auth_url: str = Field(..., description="Google authorization URL")


class GoogleUserInfo(BaseModel):
    """Parsed Google userinfo payload."""

    sub: str  # Stable Google subject ID
    email: EmailStr
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    picture: Optional[str] = None
