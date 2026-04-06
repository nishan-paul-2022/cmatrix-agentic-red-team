"""Authentication service — Google OAuth 2.0 only."""

import secrets
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional

import httpx
from jose import JWTError, jwt
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.auth import GoogleUserInfo, TokenData
from app.models.user import User

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_SCOPES = "openid email profile"


class AuthService:
    """Service for JWT management and Google OAuth operations."""

    # ------------------------------------------------------------------
    # JWT helpers
    # ------------------------------------------------------------------

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a signed JWT access token.

        Args:
            data: Payload dict; must contain a ``sub`` key (username).
            expires_delta: Token lifetime; defaults to ``ACCESS_TOKEN_EXPIRE_MINUTES``.

        Returns:
            Encoded JWT string.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """
        Verify and decode a JWT token.

        Returns:
            ``TokenData`` if the token is valid, ``None`` otherwise.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: Optional[str] = payload.get("sub")
            if username is None:
                return None
            return TokenData(username=username)
        except JWTError as exc:
            logger.error(f"JWT verification error: {exc}")
            return None

    # ------------------------------------------------------------------
    # User lookups
    # ------------------------------------------------------------------

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Return a user matched by username, or ``None``."""
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Return a user matched by email address, or ``None``."""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_google_id(db: AsyncSession, google_id: str) -> Optional[User]:
        """Return a user matched by Google subject ID, or ``None``."""
        result = await db.execute(select(User).filter(User.google_id == google_id))
        return result.scalar_one_or_none()

    # ------------------------------------------------------------------
    # Google OAuth — authorization URL
    # ------------------------------------------------------------------

    @staticmethod
    def build_google_auth_url(state: Optional[str] = None) -> str:
        """
        Build the Google OAuth 2.0 authorization URL.

        Args:
            state: CSRF-protection state token; auto-generated when not supplied.

        Returns:
            Full Google authorization URL.

        Raises:
            ValueError: If Google OAuth credentials are missing from settings.
        """
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_REDIRECT_URI:
            raise ValueError(
                "Google OAuth is not configured. "
                "Set GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI in your .env file."
            )

        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": GOOGLE_SCOPES,
            "access_type": "offline",
            "prompt": "select_account",
            "state": state or secrets.token_urlsafe(32),
        }
        return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

    # ------------------------------------------------------------------
    # Google OAuth — code exchange
    # ------------------------------------------------------------------

    @staticmethod
    async def exchange_code_for_tokens(code: str) -> dict:
        """
        Exchange the Google authorization code for access / id tokens.

        Args:
            code: Authorization code received at the callback endpoint.

        Returns:
            Google token response payload (dict).

        Raises:
            ValueError: On HTTP or API-level errors.
        """
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise ValueError("Google OAuth credentials are not configured.")

        payload = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(GOOGLE_TOKEN_URL, data=payload)

        if resp.status_code != 200:
            logger.error(f"Google token exchange failed [{resp.status_code}]: {resp.text}")
            raise ValueError("Google token exchange failed. Please try again.")

        return resp.json()

    # ------------------------------------------------------------------
    # Google OAuth — userinfo
    # ------------------------------------------------------------------

    @staticmethod
    async def fetch_google_userinfo(access_token: str) -> GoogleUserInfo:
        """
        Fetch the authenticated user's profile from Google's userinfo endpoint.

        Args:
            access_token: Valid Google OAuth 2.0 access token.

        Returns:
            Parsed ``GoogleUserInfo`` model.

        Raises:
            ValueError: On HTTP or API-level errors.
        """
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )

        if resp.status_code != 200:
            logger.error(f"Google userinfo fetch failed [{resp.status_code}]: {resp.text}")
            raise ValueError("Failed to retrieve Google user information.")

        return GoogleUserInfo(**resp.json())

    # ------------------------------------------------------------------
    # Google OAuth — get or create user
    # ------------------------------------------------------------------

    @staticmethod
    async def get_or_create_google_user(db: AsyncSession, google_info: GoogleUserInfo) -> User:
        """
        Return the existing user for this Google account, or create one.

        Lookup order:
        1. Match by ``google_id`` — fastest and most reliable.
        2. Match by ``email`` — links pre-existing accounts on first OAuth login.
        3. Create a new OAuth-only user.

        Args:
            db: Async SQLAlchemy session.
            google_info: Validated Google userinfo payload.

        Returns:
            The matched or newly-created ``User`` instance.
        """
        # 1. Existing Google-linked account
        user = await AuthService.get_user_by_google_id(db, google_info.sub)
        if user:
            # Refresh avatar if it changed
            if user.avatar_url != google_info.picture:
                user.avatar_url = google_info.picture
                await db.commit()
                await db.refresh(user)
            logger.info(f"Google OAuth login: {user.username} ({user.email})")
            return user

        # 2. Account with matching email already exists — link it
        user = await AuthService.get_user_by_email(db, str(google_info.email))
        if user:
            user.google_id = google_info.sub
            user.avatar_url = google_info.picture
            user.auth_provider = "google"
            await db.commit()
            await db.refresh(user)
            logger.info(f"Linked Google account to: {user.username} ({user.email})")
            return user

        # 3. Brand-new user — derive username from email prefix
        base = str(google_info.email).split("@")[0].lower()
        username = base
        for _ in range(20):
            if not await AuthService.get_user_by_username(db, username):
                break
            username = f"{base}_{secrets.token_hex(3)}"
        else:
            username = f"user_{secrets.token_hex(6)}"

        user = User(
            username=username,
            email=str(google_info.email),
            hashed_password=None,
            avatar_url=google_info.picture,
            google_id=google_info.sub,
            auth_provider="google",
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Created Google OAuth user: {user.username} ({user.email})")
        return user


# Global singleton
auth_service = AuthService()
