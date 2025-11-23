"""Application configuration and settings management."""

import os
from typing import List, Optional, Dict, Any
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
        ]
    )
    
    # LLM Configuration (Legacy - for backward compatibility)
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    HUGGINGFACE_MODEL: str = Field(
        default="DeepHat/DeepHat-V1-7B",
        env="HUGGINGFACE_MODEL"
    )

    # Multi-Provider LLM Configuration
    DEFAULT_LLM_PROVIDER: str = Field(default="huggingface", env="DEFAULT_LLM_PROVIDER")

    # Provider-specific configurations
    # Ollama
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    OLLAMA_MODEL: str = Field(default="gemma3:4b", env="OLLAMA_MODEL")

    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, env="OPENROUTER_API_KEY")
    OPENROUTER_MODEL: str = Field(default="x-ai/grok-4-fast:free", env="OPENROUTER_MODEL")

    # Kilo Code
    KILOCODE_TOKEN: Optional[str] = Field(default=None, env="KILOCODE_TOKEN")
    KILOCODE_MODEL: str = Field(default="x-ai/grok-code-fast-1", env="KILOCODE_MODEL")

    # Gemini (multiple instances)
    GEMINI_API_KEY_1: Optional[str] = Field(default=None, env="GEMINI_API_KEY_1")
    GEMINI_API_KEY_2: Optional[str] = Field(default=None, env="GEMINI_API_KEY_2")
    GEMINI_API_KEY_3: Optional[str] = Field(default=None, env="GEMINI_API_KEY_3")
    GEMINI_MODEL: str = Field(default="gemini-2.5-pro", env="GEMINI_MODEL")

    # Cerebras (multiple instances)
    CEREBRAS_API_KEY_1: Optional[str] = Field(default=None, env="CEREBRAS_API_KEY_1")
    CEREBRAS_API_KEY_2: Optional[str] = Field(default=None, env="CEREBRAS_API_KEY_2")
    CEREBRAS_API_KEY_3: Optional[str] = Field(default=None, env="CEREBRAS_API_KEY_3")
    CEREBRAS_MODEL: str = Field(default="gpt-oss-120b", env="CEREBRAS_MODEL")

    # Provider enable/disable flags
    ENABLE_OLLAMA: bool = Field(default=False, env="ENABLE_OLLAMA")
    ENABLE_OPENROUTER: bool = Field(default=False, env="ENABLE_OPENROUTER")
    ENABLE_KILOCODE: bool = Field(default=False, env="ENABLE_KILOCODE")
    ENABLE_GEMINI: bool = Field(default=False, env="ENABLE_GEMINI")
    ENABLE_CEREBRAS: bool = Field(default=False, env="ENABLE_CEREBRAS")
    ENABLE_HUGGINGFACE: bool = Field(default=True, env="ENABLE_HUGGINGFACE")
    
    # Paths
    BASE_DIR: str = Field(default_factory=lambda: os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DATA_DIR: str = Field(default="data")

    
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
            # Parse from string (comma-separated)
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
