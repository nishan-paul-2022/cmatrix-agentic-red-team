"""API Provider service for fetching available models from different providers."""

from typing import List, Dict, Any
import httpx
from loguru import logger

from app.models.llm import AvailableModel, APIProvider


class APIProviderService:
    """Service for fetching models from various API providers."""
    
    @staticmethod
    async def fetch_models(provider: str, api_key: str) -> List[AvailableModel]:
        """
        Fetch available models from a provider.
        
        Args:
            provider: Provider name
            api_key: API key for authentication
            
        Returns:
            List of available models
            
        Raises:
            ValueError: If provider is not supported
            HTTPException: If API request fails
        """
        provider_lower = provider.lower().replace(" ", "")
        
        if provider == APIProvider.CEREBRAS or provider_lower == "cerebras":
            return await APIProviderService._fetch_cerebras_models(api_key)
        elif provider == APIProvider.GEMINI or provider_lower == "gemini":
            return await APIProviderService._fetch_gemini_models(api_key)
        elif provider == APIProvider.HUGGING_FACE or provider_lower == "huggingface":
            return await APIProviderService._fetch_huggingface_models(api_key)
        elif provider == APIProvider.KILO_CODE or provider_lower == "kilocode":
            return await APIProviderService._fetch_kilocode_models(api_key)
        elif provider == APIProvider.OPENROUTER or provider_lower == "openrouter":
            return await APIProviderService._fetch_openrouter_models(api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @staticmethod
    async def _fetch_cerebras_models(api_key: str) -> List[AvailableModel]:
        """Fetch models from Cerebras."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.cerebras.ai/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                models = []
                for model in data.get("data", []):
                    models.append(AvailableModel(
                        id=model.get("id", ""),
                        name=model.get("id", ""),
                        description=f"Cerebras - {model.get('id', '')}",
                        context_length=model.get("context_length")
                    ))
                
                logger.info(f"Fetched {len(models)} models from Cerebras")
                return models
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch Cerebras models: {e}")
            raise
    
    @staticmethod
    async def _fetch_gemini_models(api_key: str) -> List[AvailableModel]:
        """Fetch models from Google Gemini."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                models = []
                for model in data.get("models", []):
                    # Only include generative models
                    if "generateContent" in model.get("supportedGenerationMethods", []):
                        model_name = model.get("name", "").replace("models/", "")
                        models.append(AvailableModel(
                            id=model_name,
                            name=model.get("displayName", model_name),
                            description=model.get("description", ""),
                            context_length=None
                        ))
                
                logger.info(f"Fetched {len(models)} models from Gemini")
                return models
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch Gemini models: {e}")
            raise
    
    @staticmethod
    async def _fetch_huggingface_models(api_key: str) -> List[AvailableModel]:
        """Fetch models from Hugging Face Inference API."""
        try:
            # Hugging Face doesn't have a simple "list all models" endpoint
            # We'll return a curated list of popular free inference models
            models = [
                AvailableModel(
                    id="meta-llama/Llama-3.2-3B-Instruct",
                    name="Llama 3.2 3B Instruct",
                    description="Meta's Llama 3.2 3B instruction-tuned model"
                ),
                AvailableModel(
                    id="mistralai/Mistral-7B-Instruct-v0.3",
                    name="Mistral 7B Instruct v0.3",
                    description="Mistral AI's 7B instruction model"
                ),
                AvailableModel(
                    id="google/gemma-2-2b-it",
                    name="Gemma 2 2B IT",
                    description="Google's Gemma 2 2B instruction-tuned"
                ),
                AvailableModel(
                    id="Qwen/Qwen2.5-7B-Instruct",
                    name="Qwen 2.5 7B Instruct",
                    description="Alibaba's Qwen 2.5 7B instruction model"
                ),
                AvailableModel(
                    id="microsoft/Phi-3.5-mini-instruct",
                    name="Phi-3.5 Mini Instruct",
                    description="Microsoft's Phi-3.5 mini instruction model"
                ),
            ]
            
            logger.info(f"Returning {len(models)} curated HuggingFace models")
            return models
        except Exception as e:
            logger.error(f"Failed to fetch HuggingFace models: {e}")
            raise
    
    @staticmethod
    async def _fetch_kilocode_models(api_key: str) -> List[AvailableModel]:
        """Fetch models from Kilo Code."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.kilo.codes/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                models = []
                for model in data.get("data", []):
                    models.append(AvailableModel(
                        id=model.get("id", ""),
                        name=model.get("id", ""),
                        description=f"KiloCode - {model.get('id', '')}",
                        context_length=model.get("context_length")
                    ))
                
                logger.info(f"Fetched {len(models)} models from KiloCode")
                return models
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch KiloCode models: {e}")
            raise
    
    @staticmethod
    async def _fetch_openrouter_models(api_key: str) -> List[AvailableModel]:
        """Fetch models from OpenRouter."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://openrouter.ai/api/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                models = []
                for model in data.get("data", []):
                    # Filter for free models
                    pricing = model.get("pricing", {})
                    is_free = (
                        pricing.get("prompt") == "0" or 
                        pricing.get("prompt") == 0 or
                        ":free" in model.get("id", "")
                    )
                    
                    if is_free:
                        models.append(AvailableModel(
                            id=model.get("id", ""),
                            name=model.get("name", model.get("id", "")),
                            description=model.get("description", ""),
                            context_length=model.get("context_length")
                        ))
                
                logger.info(f"Fetched {len(models)} free models from OpenRouter")
                return models
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch OpenRouter models: {e}")
            raise


# Global service instance
api_provider_service = APIProviderService()
