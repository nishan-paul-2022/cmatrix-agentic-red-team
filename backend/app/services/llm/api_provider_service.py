"""API Provider service for fetching available models from different providers."""

from loguru import logger

from app.models.llm import APIProvider, AvailableModel

from .providers.base import ProviderConfig
from .providers.cerebras import CerebrasProvider
from .providers.gemini import GeminiProvider
from .providers.huggingface import HuggingFaceProvider
from .providers.ollama import OllamaProvider
from .providers.openrouter import OpenRouterProvider


class APIProviderService:
    """Service for fetching models from various API providers."""

    # Provider class mapping
    PROVIDER_MAP = {
        APIProvider.CEREBRAS: CerebrasProvider,
        "cerebras": CerebrasProvider,
        APIProvider.GEMINI: GeminiProvider,
        "gemini": GeminiProvider,
        APIProvider.HUGGING_FACE: HuggingFaceProvider,
        "huggingface": HuggingFaceProvider,
        "hugging face": HuggingFaceProvider,
        APIProvider.OPENROUTER: OpenRouterProvider,
        "openrouter": OpenRouterProvider,
        "ollama": OllamaProvider,
    }

    @staticmethod
    async def fetch_models(provider: str, api_key: str) -> list[AvailableModel]:
        """
        Fetch available models from a provider dynamically.

        Args:
            provider: Provider name
            api_key: API key for authentication

        Returns:
            List of available models

        Raises:
            ValueError: If provider is not supported
            Exception: If API request fails
        """
        provider_normalized = provider.lower().replace(" ", "")

        # Get provider class from mapping
        provider_class = APIProviderService.PROVIDER_MAP.get(provider)
        if not provider_class:
            provider_class = APIProviderService.PROVIDER_MAP.get(provider_normalized)

        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider}")

        try:
            # Create provider config
            config = ProviderConfig(
                api_key=api_key,
                model="dummy",  # Not needed for fetching models
            )

            # Instantiate provider
            provider_instance = provider_class(config)

            # Fetch models using the provider's method
            models = provider_instance.get_available_models()

            logger.info(f"Successfully fetched {len(models)} models from {provider}")
            return models

        except Exception as e:
            logger.error(f"Failed to fetch models from {provider}: {e}")
            raise


# Global service instance
api_provider_service = APIProviderService()
