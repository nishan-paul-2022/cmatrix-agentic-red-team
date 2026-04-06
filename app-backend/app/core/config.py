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
    APP_NAME: str = Field(default="CMatrix")
    APP_VERSION: str = Field(default="1.0.0")
    APP_DESCRIPTION: str = Field(default="Agentic Red Team Security Framework")
    DEBUG: bool = Field(default=True)

    # Ports
    BACKEND_PORT: int = Field(default=3012)
    FRONTEND_PORT: int = Field(default=3011)
    POSTGRES_PORT: int = Field(default=5432)
    REDIS_PORT: int = Field(default=6379)

    # CORS
    CORS_ORIGINS: Any = Field(default=["*"])

    # Paths
    BASE_DIR: str = Field(
        default_factory=lambda: os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    DATA_DIR: str = Field(default="app/data")

    # Demo Configuration
    AUTH_CONFIG_FILE: str = Field(default="config/auth.yml")

    # Database
    DATABASE_URL: str = Field(default="postgresql+asyncpg://cmatrix:cmatrix@localhost:5432/cmatrix")

    # Security & JWT
    SECRET_KEY: str = Field(default="cmatrix-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=10080)

    # Celery & Background Jobs
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/2")

    # Vector Database (Qdrant)
    QDRANT_HOST: str = Field(default="localhost")
    QDRANT_PORT: int = Field(default=6333)
    QDRANT_URL: str = Field(default="http://localhost:6333")
    QDRANT_COLLECTION_NAME: str = Field(default="cmatrix_memory")

    # Embeddings
    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2")
    EMBEDDING_DEVICE: str = Field(default="cpu")

    # URLs (used for redirects, CORS, and OAuth)
    FRONTEND_URL: str = Field(default="http://localhost:3011")
    BACKEND_URL: str = Field(default="http://localhost:3012")

    # Google OAuth 2.0
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None)
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None)
    GOOGLE_REDIRECT_URI: Optional[str] = Field(default=None)

    # External APIs
    NVD_API_KEY: Optional[str] = Field(default=None)

    # Command Execution
    COMMAND_TIMEOUT: int = Field(default=30)
    ENABLE_SUDO: bool = Field(default=False)

    # Logging
    LOG_LEVEL: str = Field(default="INFO")

    # Optimization: Cache
    CACHE_ENABLED: bool = Field(default=True)
    CACHE_SIMILARITY_THRESHOLD: float = Field(default=0.85)
    CACHE_TTL_SECONDS: int = Field(default=3600)
    CACHE_MAX_SIZE: int = Field(default=1000)
    REDIS_HOST: str = Field(default="localhost")
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    REDIS_SSL: bool = Field(default=False)
    REDIS_USERNAME: Optional[str] = Field(default=None)

    # Optimization: Backpressure
    BP_ENABLED: bool = Field(default=True)
    BP_BATCH_SIZE: int = Field(default=10)
    BP_BATCH_TIMEOUT_MS: int = Field(default=100)
    BP_MAX_EVENTS_PER_SEC: int = Field(default=50)
    BP_COMPRESSION_THRESHOLD: int = Field(default=2000)

    # Optimization: Token Optimizer
    TOKEN_OPT_ENABLED: bool = Field(default=True)
    TOKEN_SUMMARIZATION_THRESHOLD: int = Field(default=4000)
    TOKEN_MAX_CONTEXT_MESSAGES: int = Field(default=10)
    TOKEN_DYNAMIC_TOOL_FILTERING: bool = Field(default=True)
    TOKEN_COMPRESS_PROMPTS: bool = Field(default=True)
    TOKEN_TRACK_COSTS: bool = Field(default=True)
    TOKEN_MODEL_NAME: str = Field(default="gpt-4o")
    TOKEN_INPUT_COST: float = Field(default=0.01)
    TOKEN_OUTPUT_COST: float = Field(default=0.03)

    # Reasoning: ReWOO
    REWOO_CACHE_TTL: int = Field(default=3600)
    REWOO_ENABLE_CACHE: bool = Field(default=True)
    REWOO_ENABLE_TEMPLATES: bool = Field(default=True)

    # LLM Provider Defaults
    LLM_TEMPERATURE: float = Field(default=0.7)
    LLM_MAX_TOKENS: int = Field(default=4096)
    LLM_TIMEOUT: int = Field(default=60)
    LLM_RETRY_ATTEMPTS: int = Field(default=3)
    LLM_RETRY_DELAY: float = Field(default=1.0)

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
