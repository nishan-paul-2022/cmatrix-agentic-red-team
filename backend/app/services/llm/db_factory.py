"""Database-aware LLM Provider Factory - Simplified."""

from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm.config_profile_service import config_profile_service

from .providers import (
    CerebrasProvider,
    GeminiProvider,
    HuggingFaceProvider,
    LLMProvider,
    OllamaProvider,
    OpenRouterProvider,
    ProviderConfig,
)


class DatabaseLLMProviderFactory:
    """Factory for creating LLM providers from database configuration."""

    def __init__(self):
        """Initialize the provider factory."""
        self._provider_map = {
            "huggingface": HuggingFaceProvider,
            "Hugging Face": HuggingFaceProvider,
            "ollama": OllamaProvider,
            "openrouter": OpenRouterProvider,
            "Openrouter": OpenRouterProvider,
            "gemini": GeminiProvider,
            "Gemini": GeminiProvider,
            "cerebras": CerebrasProvider,
            "Cerebras": CerebrasProvider,
        }
        logger.info("🤖 Database LLM Provider Factory initialized")

    async def get_active_provider(self, db: AsyncSession, user_id: int) -> Optional[LLMProvider]:
        """
        Get user's active LLM provider.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Active provider instance or None
        """
        # Get active profile
        profile = await config_profile_service.get_active_profile(db, user_id)

        if not profile:
            logger.warning(f"No active profile found for user {user_id}")
            return None

        if not profile.api_key or not profile.selected_model_name:
            logger.warning(f"Active profile {profile.id} missing API key or model")
            return None

        # Create provider config
        config = ProviderConfig(
            api_key=profile.api_key,
            model=profile.selected_model_name,
            base_url=None,
            temperature=0.4,
            max_tokens=4096,
        )

        # Get provider class
        provider_class = self._provider_map.get(profile.api_provider)
        if not provider_class:
            logger.error(f"Unknown provider: {profile.api_provider}")
            return None

        # Create and return provider instance
        try:
            provider = provider_class(config)
            logger.info(f"✅ Created {profile.api_provider} provider for user {user_id}")
            return provider
        except Exception as e:
            logger.error(f"Failed to create provider {profile.api_provider}: {e}")
            return None


# Global factory instance
_db_provider_factory: Optional[DatabaseLLMProviderFactory] = None


def get_db_provider_factory() -> DatabaseLLMProviderFactory:
    """Get or create global database provider factory instance."""
    global _db_provider_factory
    if _db_provider_factory is None:
        _db_provider_factory = DatabaseLLMProviderFactory()
    return _db_provider_factory
