"""Application configuration and settings management."""

import os
from functools import lru_cache
from typing import Any, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = Field(..., env="APP_NAME")
    APP_VERSION: str = Field(..., env="APP_VERSION")
    APP_DESCRIPTION: str = Field(..., env="APP_DESCRIPTION")
    DEBUG: bool = Field(..., env="DEBUG")

    # Ports
    BACKEND_PORT: int = Field(..., env="BACKEND_PORT")
    FRONTEND_PORT: int = Field(..., env="FRONTEND_PORT")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")

    # CORS
    CORS_ORIGINS: Any = Field(..., env="CORS_ORIGINS")

    # Paths
    BASE_DIR: str = Field(
        default_factory=lambda: os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    DATA_DIR: str = Field(..., env="DATA_DIR")

    # Demo Configuration
    AUTH_CONFIG_FILE: str = Field(..., env="AUTH_CONFIG_FILE")

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Security & JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Celery & Background Jobs
    CELERY_BROKER_URL: str = Field(..., env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(..., env="CELERY_RESULT_BACKEND")

    # Vector Database (Qdrant)
    QDRANT_HOST: str = Field(..., env="QDRANT_HOST")
    QDRANT_PORT: int = Field(..., env="QDRANT_PORT")
    QDRANT_URL: str = Field(..., env="QDRANT_URL")
    QDRANT_COLLECTION_NAME: str = Field(..., env="QDRANT_COLLECTION_NAME")

    # Embeddings
    EMBEDDING_MODEL: str = Field(..., env="EMBEDDING_MODEL")
    EMBEDDING_DEVICE: str = Field(..., env="EMBEDDING_DEVICE")

    # External APIs
    NVD_API_KEY: Optional[str] = Field(default=None, env="NVD_API_KEY")

    # Command Execution
    COMMAND_TIMEOUT: int = Field(..., env="COMMAND_TIMEOUT")
    ENABLE_SUDO: bool = Field(..., env="ENABLE_SUDO")

    # Logging
    LOG_LEVEL: str = Field(..., env="LOG_LEVEL")

    # Optimization: Cache
    CACHE_ENABLED: bool = Field(..., env="CACHE_ENABLED")
    CACHE_SIMILARITY_THRESHOLD: float = Field(..., env="CACHE_SIMILARITY_THRESHOLD")
    CACHE_TTL_SECONDS: int = Field(..., env="CACHE_TTL_SECONDS")
    CACHE_MAX_SIZE: int = Field(..., env="CACHE_MAX_SIZE")
    REDIS_HOST: str = Field(..., env="REDIS_HOST")

    # Optimization: Backpressure
    BP_ENABLED: bool = Field(..., env="BP_ENABLED")
    BP_BATCH_SIZE: int = Field(..., env="BP_BATCH_SIZE")
    BP_BATCH_TIMEOUT_MS: int = Field(..., env="BP_BATCH_TIMEOUT_MS")
    BP_MAX_EVENTS_PER_SEC: int = Field(..., env="BP_MAX_EVENTS_PER_SEC")
    BP_COMPRESSION_THRESHOLD: int = Field(..., env="BP_COMPRESSION_THRESHOLD")

    # Optimization: Token Optimizer
    TOKEN_OPT_ENABLED: bool = Field(..., env="TOKEN_OPT_ENABLED")
    TOKEN_SUMMARIZATION_THRESHOLD: int = Field(..., env="TOKEN_SUMMARIZATION_THRESHOLD")
    TOKEN_MAX_CONTEXT_MESSAGES: int = Field(..., env="TOKEN_MAX_CONTEXT_MESSAGES")
    TOKEN_DYNAMIC_TOOL_FILTERING: bool = Field(..., env="TOKEN_DYNAMIC_TOOL_FILTERING")
    TOKEN_COMPRESS_PROMPTS: bool = Field(..., env="TOKEN_COMPRESS_PROMPTS")
    TOKEN_TRACK_COSTS: bool = Field(..., env="TOKEN_TRACK_COSTS")
    TOKEN_MODEL_NAME: str = Field(..., env="TOKEN_MODEL_NAME")
    TOKEN_INPUT_COST: float = Field(..., env="TOKEN_INPUT_COST")
    TOKEN_OUTPUT_COST: float = Field(..., env="TOKEN_OUTPUT_COST")

    # Reasoning: ReWOO
    REWOO_CACHE_TTL: int = Field(..., env="REWOO_CACHE_TTL")
    REWOO_ENABLE_CACHE: bool = Field(..., env="REWOO_ENABLE_CACHE")
    REWOO_ENABLE_TEMPLATES: bool = Field(..., env="REWOO_ENABLE_TEMPLATES")

    # LLM Provider Defaults (used when constructing ProviderConfig)
    LLM_TEMPERATURE: float = Field(..., env="LLM_TEMPERATURE")
    LLM_MAX_TOKENS: int = Field(..., env="LLM_MAX_TOKENS")
    LLM_TIMEOUT: int = Field(..., env="LLM_TIMEOUT")
    LLM_RETRY_ATTEMPTS: int = Field(..., env="LLM_RETRY_ATTEMPTS")
    LLM_RETRY_DELAY: float = Field(..., env="LLM_RETRY_DELAY")

    class Config:
        """Pydantic configuration."""

        # Resolve path to the root .env regardless of CWD.
        # __file__ = app-backend/app/core/config.py → go up 4 levels to project root.
        _root = os.path.dirname(  # project root
            os.path.dirname(  # app-backend/
                os.path.dirname(  # app/
                    os.path.dirname(os.path.abspath(__file__))  # core/
                )
            )
        )
        env_file = os.path.join(_root, ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated string into a list."""
        if isinstance(v, str):
            # Remove brackets and quotes if present
            v = v.replace("[", "").replace("]", "").replace('"', "").replace("'", "")
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
