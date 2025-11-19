"""Application configuration and settings management."""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "DeepHat Agent API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI Agent with LangGraph and tool calling"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    RELOAD: bool = Field(default=True, env="RELOAD")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        env="CORS_ORIGINS"
    )
    
    # LLM Configuration
    HUGGINGFACE_API_KEY: str = Field(..., env="HUGGINGFACE_API_KEY")
    HUGGINGFACE_MODEL: str = Field(
        default="DeepHat/DeepHat-V1-7B",
        env="HUGGINGFACE_MODEL"
    )
    
    # Paths
    BASE_DIR: str = Field(default_factory=lambda: os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DATA_DIR: str = Field(default="data")
    LOGS_DIR: str = Field(default="logs")
    AUDIT_LOGS_DIR: str = Field(default="logs/audit_logs")
    
    # Demo Configuration
    DEMOS_FILE: str = Field(default="data/demos.json")
    AUTH_CONFIG_FILE: str = Field(default="data/auth_config.json")
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://cmatrix:cmatrix@localhost:5432/cmatrix",
        env="DATABASE_URL"
    )
    
    # Security & JWT
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production-make-it-very-long-and-random",
        env="SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=10080, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # 7 days

    
    # Command Execution
    COMMAND_TIMEOUT: int = Field(default=30, env="COMMAND_TIMEOUT")
    ENABLE_SUDO: bool = Field(default=False, env="ENABLE_SUDO")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
