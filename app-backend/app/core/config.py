"""Application configuration and settings management."""

import os
from functools import lru_cache
from typing import Any, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            ),
            ".env",
        ),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = Field(...)
    APP_VERSION: str = Field(...)
    APP_DESCRIPTION: str = Field(...)
    DEBUG: bool = Field(...)

    # Ports
    BACKEND_PORT: int = Field(...)
    FRONTEND_PORT: int = Field(...)
    POSTGRES_PORT: int = Field(...)
    REDIS_PORT: int = Field(...)

    # CORS
    CORS_ORIGINS: Any = Field(...)

    # Paths
    BASE_DIR: str = Field(
        default_factory=lambda: os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    DATA_DIR: str = Field(...)

    # Demo Configuration
    AUTH_CONFIG_FILE: str = Field(...)

    # Database
    DATABASE_URL: str = Field(...)

    # Security & JWT
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(...)

    # Celery & Background Jobs
    CELERY_BROKER_URL: str = Field(...)
    CELERY_RESULT_BACKEND: str = Field(...)

    # Vector Database (Qdrant)
    QDRANT_HOST: str = Field(...)
    QDRANT_PORT: int = Field(...)
    QDRANT_URL: str = Field(...)
    QDRANT_COLLECTION_NAME: str = Field(...)

    # Embeddings
    EMBEDDING_MODEL: str = Field(...)
    EMBEDDING_DEVICE: str = Field(...)

    # External APIs
    NVD_API_KEY: Optional[str] = Field(default=None)

    # Command Execution
    COMMAND_TIMEOUT: int = Field(...)
    ENABLE_SUDO: bool = Field(...)

    # Logging
    LOG_LEVEL: str = Field(...)

    # Optimization: Cache
    CACHE_ENABLED: bool = Field(...)
    CACHE_SIMILARITY_THRESHOLD: float = Field(...)
    CACHE_TTL_SECONDS: int = Field(...)
    CACHE_MAX_SIZE: int = Field(...)
    REDIS_HOST: str = Field(...)
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    REDIS_SSL: bool = Field(default=False)
    REDIS_USERNAME: Optional[str] = Field(default=None)

    # Optimization: Backpressure
    BP_ENABLED: bool = Field(...)
    BP_BATCH_SIZE: int = Field(...)
    BP_BATCH_TIMEOUT_MS: int = Field(...)
    BP_MAX_EVENTS_PER_SEC: int = Field(...)
    BP_COMPRESSION_THRESHOLD: int = Field(...)

    # Optimization: Token Optimizer
    TOKEN_OPT_ENABLED: bool = Field(...)
    TOKEN_SUMMARIZATION_THRESHOLD: int = Field(...)
    TOKEN_MAX_CONTEXT_MESSAGES: int = Field(...)
    TOKEN_DYNAMIC_TOOL_FILTERING: bool = Field(...)
    TOKEN_COMPRESS_PROMPTS: bool = Field(...)
    TOKEN_TRACK_COSTS: bool = Field(...)
    TOKEN_MODEL_NAME: str = Field(...)
    TOKEN_INPUT_COST: float = Field(...)
    TOKEN_OUTPUT_COST: float = Field(...)

    # Reasoning: ReWOO
    REWOO_CACHE_TTL: int = Field(...)
    REWOO_ENABLE_CACHE: bool = Field(...)
    REWOO_ENABLE_TEMPLATES: bool = Field(...)

    # LLM Provider Defaults
    LLM_TEMPERATURE: float = Field(...)
    LLM_MAX_TOKENS: int = Field(...)
    LLM_TIMEOUT: int = Field(...)
    LLM_RETRY_ATTEMPTS: int = Field(...)
    LLM_RETRY_DELAY: float = Field(...)

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated string into a list."""
        if isinstance(v, str):
            v = v.replace("[", "").replace("]", "").replace('"', "").replace("'", "")
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
