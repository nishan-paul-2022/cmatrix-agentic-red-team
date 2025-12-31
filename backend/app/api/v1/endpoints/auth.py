"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.auth import SetupStatusResponse, Token, UserLogin, UserResponse, UserSetup
from app.services.auth import auth_service

router = APIRouter(tags=["Authentication"])
security = HTTPBearer()


@router.get(
    "/setup/status",
    response_model=SetupStatusResponse,
    summary="Check Setup Status",
    description="Check if initial user setup is complete",
)
async def get_setup_status(db: AsyncSession = Depends(get_db)):
    """Check if the system has been set up with initial credentials."""
    is_complete = await auth_service.is_setup_complete(db)
    return SetupStatusResponse(is_setup_complete=is_complete)


@router.post(
    "/setup",
    response_model=Token,
    summary="Initial Setup",
    description="Set up the first user credentials (only works if no users exist)",
    status_code=status.HTTP_201_CREATED,
)
async def setup_initial_user(user_data: UserSetup, db: AsyncSession = Depends(get_db)):
    """
    Set up the initial user credentials.
    This endpoint only works if no users exist in the system.
    """
    # Check if setup is already complete
    is_complete = await auth_service.is_setup_complete(db)
    if is_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Setup already complete. User already exists.",
        )

    # Check if username already exists (extra safety)
    existing_user = await auth_service.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    # Create the user
    try:
        user = await auth_service.create_user(db, user_data.username, user_data.password)

        # Create access token
        access_token = auth_service.create_access_token(data={"sub": user.username})

        logger.info(f"Initial setup completed for user: {user.username}")

        return Token(access_token=access_token, token_type="bearer")

    except Exception as e:
        logger.error(f"Error during setup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user"
        )


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate with username and password",
)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token."""
    # Check if setup is complete
    is_complete = await auth_service.is_setup_complete(db)
    if not is_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System not set up. Please complete initial setup first.",
        )

    # Authenticate user
    user = await auth_service.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = auth_service.create_access_token(data={"sub": user.username})

    logger.info(f"User logged in: {user.username}")

    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User",
    description="Get current authenticated user information",
)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user."""
    # Verify token
    token_data = auth_service.verify_token(credentials.credentials)
    if token_data is None or token_data.username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = await auth_service.get_user_by_username(db, token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
    )
