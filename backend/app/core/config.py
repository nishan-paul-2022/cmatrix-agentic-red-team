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

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=[
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
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://cmatrix:cmatrix@localhost:5432/cmatrix", env="DATABASE_URL"
    )

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
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/1", env="CELERY_RESULT_BACKEND"
    )

    # Vector Database (Qdrant)
    QDRANT_HOST: str = Field(default="localhost", env="QDRANT_HOST")
    QDRANT_PORT: int = Field(default=6333, env="QDRANT_PORT")
    QDRANT_URL: str = Field(default="http://localhost:6333", env="QDRANT_URL")
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

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            # Parse from string (comma-separated)
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
