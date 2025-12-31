"""Authentication service for user management and JWT tokens."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.auth import TokenData
from app.models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.

        Args:
            data: Data to encode in token
            expires_delta: Token expiration time

        Returns:
            JWT token string
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            TokenData if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return TokenData(username=username)
        except JWTError as e:
            logger.error(f"JWT verification error: {e}")
            return None

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            db: Database session
            username: Username to search for

        Returns:
            User if found, None otherwise
        """
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user.

        Args:
            db: Database session
            username: Username
            password: Password

        Returns:
            User if authenticated, None otherwise
        """
        user = await AuthService.get_user_by_username(db, username)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    async def create_user(db: AsyncSession, username: str, password: str) -> User:
        """
        Create a new user.

        Args:
            db: Database session
            username: Username
            password: Plain text password

        Returns:
            Created user
        """
        hashed_password = AuthService.get_password_hash(password)
        user = User(username=username, hashed_password=hashed_password, is_active=True)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Created user: {username}")
        return user

    @staticmethod
    async def is_setup_complete(db: AsyncSession) -> bool:
        """
        Check if initial setup is complete (i.e., at least one user exists).

        Args:
            db: Database session

        Returns:
            True if setup is complete
        """
        result = await db.execute(select(User).limit(1))
        user = result.scalar_one_or_none()
        return user is not None

    @staticmethod
    async def get_user_count(db: AsyncSession) -> int:
        """
        Get total number of users.

        Args:
            db: Database session

        Returns:
            Number of users
        """
        from sqlalchemy import func

        result = await db.execute(select(func.count(User.id)))
        return result.scalar_one()


# Global auth service instance
auth_service = AuthService()
