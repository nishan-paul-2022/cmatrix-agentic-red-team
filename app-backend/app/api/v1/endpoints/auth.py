"""Authentication endpoints — Google OAuth 2.0 only."""

import secrets

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.auth import GoogleOAuthInitResponse, UserResponse
from app.services.auth import auth_service

router = APIRouter(tags=["Authentication"])
security = HTTPBearer()


# ---------------------------------------------------------------------------
# Current user
# ---------------------------------------------------------------------------


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User",
    description="Return the currently authenticated user's profile.",
)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Decode the Bearer JWT and return the user's profile."""
    token_data = auth_service.verify_token(credentials.credentials)
    if token_data is None or token_data.username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await auth_service.get_user_by_username(db, token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar_url=user.avatar_url,
        auth_provider=user.auth_provider,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
    )


# ---------------------------------------------------------------------------
# Google OAuth 2.0
# ---------------------------------------------------------------------------


@router.get(
    "/google/login",
    response_model=GoogleOAuthInitResponse,
    summary="Initiate Google OAuth Login",
    description=(
        "Returns the Google authorization URL. "
        "The frontend redirects the user's browser to this URL to begin the OAuth flow."
    ),
)
async def google_login() -> GoogleOAuthInitResponse:
    """Generate and return the Google OAuth authorization URL."""
    try:
        state = secrets.token_urlsafe(32)
        auth_url = auth_service.build_google_auth_url(state=state)
        return GoogleOAuthInitResponse(auth_url=auth_url)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )


@router.get(
    "/google/callback",
    summary="Google OAuth Callback",
    description=(
        "Google redirects here after the user grants access. "
        "Exchanges the authorization code for a CMatrix JWT and redirects to the frontend."
    ),
    response_class=RedirectResponse,
    include_in_schema=True,
)
async def google_callback(
    code: str = Query(None, description="Authorization code from Google"),
    state: str = Query(None, description="CSRF state token"),
    error: str = Query(None, description="Error string returned by Google"),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """
    Handle Google OAuth 2.0 callback.

    Flow:
        1. Handle any error returned by Google.
        2. Exchange ``code`` → Google access token.
        3. Fetch user profile from Google's userinfo endpoint.
        4. Get or create the CMatrix user record.
        5. Issue a signed CMatrix JWT.
        6. Redirect the browser to ``{FRONTEND_URL}/auth/callback?token=<jwt>``.
           On error redirects to ``{FRONTEND_URL}/auth/callback?error=<reason>``.
    """
    frontend_url = settings.FRONTEND_URL.rstrip("/")
    error_base = f"{frontend_url}/auth/callback?error="

    # Google returned an error (e.g. user denied access)
    if error:
        logger.warning(f"Google OAuth returned error: {error}")
        return RedirectResponse(
            url=f"{error_base}{error}",
            status_code=status.HTTP_302_FOUND,
        )

    if not code:
        logger.warning("Google OAuth callback called without an authorization code.")
        return RedirectResponse(
            url=f"{error_base}missing_code",
            status_code=status.HTTP_302_FOUND,
        )

    try:
        # Step 1 — exchange authorization code for tokens
        token_response = await auth_service.exchange_code_for_tokens(code)
        google_access_token: str = token_response.get("access_token", "")

        if not google_access_token:
            raise ValueError("Google token response contained no access_token.")

        # Step 2 — fetch user profile
        google_user = await auth_service.fetch_google_userinfo(google_access_token)

        if not google_user.email_verified:
            logger.warning(f"Unverified Google email attempted login: {google_user.email}")
            return RedirectResponse(
                url=f"{error_base}email_not_verified",
                status_code=status.HTTP_302_FOUND,
            )

        # Step 3 — get or create CMatrix user
        user = await auth_service.get_or_create_google_user(db, google_user)

        # Step 4 — issue CMatrix JWT
        jwt_token = auth_service.create_access_token(data={"sub": user.username})

        logger.info(f"Successful Google OAuth login: {user.username} ({user.email})")

        # Step 5 — redirect to frontend callback route with token
        return RedirectResponse(
            url=f"{frontend_url}/auth/callback?token={jwt_token}",
            status_code=status.HTTP_302_FOUND,
        )

    except ValueError as exc:
        logger.error(f"Google OAuth callback ValueError: {exc}")
        return RedirectResponse(
            url=f"{error_base}oauth_failed",
            status_code=status.HTTP_302_FOUND,
        )
    except Exception as exc:
        logger.error(f"Unexpected Google OAuth callback error: {exc}", exc_info=True)
        return RedirectResponse(
            url=f"{error_base}server_error",
            status_code=status.HTTP_302_FOUND,
        )
