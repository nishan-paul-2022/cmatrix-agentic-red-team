"""Application configuration and settings management."""

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "CMatrix"
    APP_VERSION: str = "0.0.1"
    APP_DESCRIPTION: str = "AI Agent with LangGraph and tool calling"
    DEBUG: bool = Field(default=False, env="DEBUG")

    # Ports
    BACKEND_PORT: int = Field(default=8000, env="BACKEND_PORT")
    FRONTEND_PORT: int = Field(default=3000, env="FRONTEND_PORT")
    POSTGRES_PORT: int = Field(default=5432, env="POSTGRES_PORT")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    # Paths
    BASE_DIR: str = Field(
        default_factory=lambda: os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    DATA_DIR: str = Field(default="data")

    # Demo Configuration
    AUTH_CONFIG_FILE: str = Field(default="data/auth_config.json")

    # Database
    DATABASE_URL: str = Field(default="${COMPUTE}", env="DATABASE_URL")

    # Security & JWT
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production-make-it-very-long-and-random",
        env="SECRET_KEY",
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=10080, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )  # 7 days

    # Celery & Background Jobs
    CELERY_BROKER_URL: str = Field(default="${COMPUTE}", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="${COMPUTE}", env="CELERY_RESULT_BACKEND")

    # Vector Database (Qdrant)
    QDRANT_HOST: str = Field(default="localhost", env="QDRANT_HOST")
    QDRANT_PORT: int = Field(default=6333, env="QDRANT_PORT")
    QDRANT_URL: str = Field(default="${COMPUTE}", env="QDRANT_URL")
    QDRANT_COLLECTION_NAME: str = Field(default="cmatrix_memory", env="QDRANT_COLLECTION_NAME")

    # Embeddings
    EMBEDDING_MODEL: str = Field(default="BAAI/bge-base-en-v1.5", env="EMBEDDING_MODEL")
    EMBEDDING_DEVICE: str = Field(default="cpu", env="EMBEDDING_DEVICE")

    # External APIs
    NVD_API_KEY: Optional[str] = Field(default=None, env="NVD_API_KEY")

    # Command Execution
    COMMAND_TIMEOUT: int = Field(default=30, env="COMMAND_TIMEOUT")
    ENABLE_SUDO: bool = Field(default=False, env="ENABLE_SUDO")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @validator("DATABASE_URL", pre=True, always=True)
    def compute_db_url(cls, v, values):
        """Compute database URL if not provided or contains ${PORT} placeholders."""
        if v and not v.startswith("${"):
            return v
        port = values.get("POSTGRES_PORT", 5432)
        user = os.getenv("POSTGRES_USER", "cmatrix")
        pw = os.getenv("POSTGRES_PASSWORD", "cmatrix")
        db = os.getenv("POSTGRES_DB", "cmatrix")
        return f"postgresql+asyncpg://{user}:{pw}@localhost:{port}/{db}"

    @validator("CELERY_BROKER_URL", pre=True, always=True)
    def compute_broker_url(cls, v, values):
        """Compute celery broker URL if not provided."""
        if v and not v.startswith("${"):
            return v
        port = values.get("REDIS_PORT", 6379)
        return f"redis://localhost:{port}/0"

    @validator("CELERY_RESULT_BACKEND", pre=True, always=True)
    def compute_backend_url(cls, v, values):
        """Compute celery result backend URL if not provided."""
        if v and not v.startswith("${"):
            return v
        port = values.get("REDIS_PORT", 6379)
        return f"redis://localhost:{port}/1"

    @validator("QDRANT_URL", pre=True, always=True)
    def compute_qdrant_url(cls, v, values):
        """Compute Qdrant URL if not provided."""
        if v and not v.startswith("${"):
            return v
        host = values.get("QDRANT_HOST", "localhost")
        port = values.get("QDRANT_PORT", 6333)
        return f"http://{host}:{port}"

    @validator("CORS_ORIGINS", pre=True, always=True)
    def compute_cors_origins(cls, v, values):
        """Compute CORS origins using FRONTEND_PORT."""
        if v and not isinstance(v, list):
            # Parse from comma-separated string if provided
            v = [origin.strip() for origin in v.split(",")]

        if v:
            return v

        port = values.get("FRONTEND_PORT", 3000)
        return [
            f"http://localhost:{port}",
            f"http://127.0.0.1:{port}",
        ]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
