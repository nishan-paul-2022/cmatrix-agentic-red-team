"""HuggingFace LLM provider (migrated from existing implementation)."""

from typing import Any

import requests
from loguru import logger

from app.models.llm import AvailableModel

from .base import LLMProvider, Message, ProviderConfig, StreamingProviderMixin


class HuggingFaceProvider(LLMProvider, StreamingProviderMixin):
    """HuggingFace provider for Router API with chat completions."""

    def __init__(self, config: ProviderConfig):
        """
        Initialize HuggingFace provider.

        Args:
            config: Provider configuration with API key and model
        """
        super().__init__(config)

        # Validate configuration
        if not self.config.api_key:
            raise ValueError("API key must be specified for HuggingFace provider")

        # Model is optional when just fetching available models
        if not self.config.model:
            logger.warning("No model specified for HuggingFace provider (OK for fetching models)")
            self.model = None
        else:
            self.model = self.config.model

        # Use chat completions endpoint for all models
        self.endpoint = "https://router.huggingface.co/v1/chat/completions"

        logger.info(f"🤗 HuggingFace provider initialized with model: {self.model}")

    def invoke(self, messages: list[Message], **kwargs) -> str:
        """
        Invoke HuggingFace model using chat completions format.

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Returns:
            Response text
        """
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        # Use chat completions format for all models
        payload = {
            "model": self.model,
            "messages": self._prepare_messages(messages),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens or 512),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "stream": False,
        }

        def make_request():
            response = requests.post(
                self.endpoint, json=payload, headers=headers, timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()

        result = self._retry_request(make_request)

        # OpenAI-compatible format
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"Unexpected response format from HuggingFace: {result}")

    def invoke_stream(self, messages: list[Message], **kwargs):
        """
        Invoke HuggingFace model with streaming (not natively supported by Router API).

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Yields:
            Response chunks (simulated for compatibility)
        """
        # HuggingFace Router API doesn't support streaming natively
        # For compatibility, we'll do non-streaming and yield the result
        try:
            result = self.invoke(messages, **kwargs)
            # Yield the result as a single chunk for compatibility
            yield result
        except Exception as e:
            logger.error(f"Error in HuggingFace streaming: {str(e)}")
            raise

    def get_available_models(self) -> list[AvailableModel]:
        """
        Get list of available FREE models from HuggingFace Router API.

        Filters for models that are likely free-tier eligible:
        - Models smaller than 10GB (free serverless inference)
        - Popular open-source models with free access
        - Excludes large commercial models

        Returns:
            List of AvailableModel objects (free models only)
        """
        try:
            url = "https://router.huggingface.co/v1/models"
            headers = {"Authorization": f"Bearer {self.config.api_key}"}

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Known free model patterns (commonly available for free inference)
            free_model_patterns = [
                "meta-llama/Llama-3.2",  # Smaller Llama models
                "mistralai/Mistral-7B",
                "google/gemma-2-2b",
                "Qwen/Qwen2.5-7B",
                "microsoft/Phi-3",
                "HuggingFaceH4/zephyr-7b",
                "tiiuae/falcon-7b",
            ]

            # Exclude large/commercial model patterns
            exclude_patterns = [
                "70b",
                "70B",  # 70B models are too large
                "405b",
                "405B",  # Very large models
                "gpt-4",
                "claude",  # Commercial models
                "gemini-pro",  # Commercial
                "embedding",
                "embed",
                "vision",
                "image",
                "whisper",
                "audio",
                "clip",
                "stable-diffusion",
                "sdxl",
            ]

            models = []
            if "data" in data:
                for model in data["data"]:
                    if "id" in model:
                        model_id = model["id"].lower()

                        is_free_pattern = any(
                            pattern.lower() in model_id for pattern in free_model_patterns
                        )
                        is_excluded = any(
                            pattern.lower() in model_id for pattern in exclude_patterns
                        )

                        if is_free_pattern or not is_excluded:
                            models.append(
                                AvailableModel(
                                    id=model["id"],
                                    name=model.get("name", model["id"]),
                                    description=model.get(
                                        "description", f"HuggingFace - {model['id']}"
                                    ),
                                    context_length=model.get("context_length"),
                                )
                            )

            models.sort(key=lambda model: model.id.lower())

            logger.info(f"Found {len(models)} free text generation models for HuggingFace")
            return models
        except Exception as e:
            logger.error(f"Failed to get HuggingFace models: {str(e)}")
            return []

    def _prepare_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """
        Prepare messages for HuggingFace format.

        Args:
            messages: List of Message objects

        Returns:
            OpenAI-compatible message format for HuggingFace Router
        """
        prepared_messages = []

        # Add system message if not present
        has_system = any(msg.role == "system" for msg in messages)
        if not has_system:
            prepared_messages.append(
                {"role": "system", "content": "You are a helpful AI assistant."}
            )

        # Add user messages
        for msg in messages:
            prepared_messages.append({"role": msg.role, "content": msg.content})

        return prepared_messages
