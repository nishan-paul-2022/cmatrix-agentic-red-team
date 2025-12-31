"""OpenRouter LLM provider for accessing various models through OpenRouter API."""

from typing import Any

import requests
from loguru import logger

from app.models.llm import AvailableModel

from .base import LLMProvider, Message, ProviderConfig, StreamingProviderMixin


class OpenRouterProvider(LLMProvider, StreamingProviderMixin):
    """OpenRouter provider for accessing various LLM models."""

    def __init__(self, config: ProviderConfig):
        """
        Initialize OpenRouter provider.

        Args:
            config: Provider configuration with API key and model
        """
        super().__init__(config)
        self.base_url = "https://openrouter.ai/api/v1"

        # Validate configuration
        if not self.config.api_key:
            raise ValueError("API key must be specified for OpenRouter provider")

        # Model is optional when just fetching available models
        if not self.config.model:
            logger.warning("No model specified for OpenRouter provider (OK for fetching models)")

        logger.info(f"🔄 OpenRouter provider initialized with model: {self.config.model}")

    def invoke(self, messages: list[Message], **kwargs) -> str:
        """
        Invoke OpenRouter model.

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Returns:
            Response text
        """
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://cmatrix.dev",  # Optional referrer
            "X-Title": "CMatrix Agent API",  # Optional title
        }

        payload = {
            "model": self.config.model,
            "messages": self._prepare_messages(messages),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens or 512),
            "stream": False,
        }

        def make_request():
            response = requests.post(
                url, headers=headers, json=payload, timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()

        result = self._retry_request(make_request)

        # OpenAI-compatible format
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"Unexpected response format from OpenRouter: {result}")

    def invoke_stream(self, messages: list[Message], **kwargs):
        """
        Invoke OpenRouter model with streaming.

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Yields:
            Response chunks
        """
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://cmatrix.dev",
            "X-Title": "CMatrix Agent API",
        }

        payload = {
            "model": self.config.model,
            "messages": self._prepare_messages(messages),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens or 512),
            "stream": True,
        }

        def make_request():
            response = requests.post(
                url, headers=headers, json=payload, timeout=self.config.timeout, stream=True
            )
            response.raise_for_status()
            return response

        response = self._retry_request(make_request)

        try:
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]  # Remove 'data: ' prefix

                    if line.strip() == "[DONE]":
                        break

                    try:
                        chunk = requests.utils.json.loads(line)
                        if "choices" in chunk and len(chunk["choices"]) > 0:
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except requests.utils.json.JSONDecodeError:
                        continue  # Skip non-JSON lines
        except Exception as e:
            logger.error(f"Error in OpenRouter streaming: {str(e)}")
            raise

    def get_available_models(self) -> list[AvailableModel]:
        """
        Get list of available FREE models from OpenRouter.

        Filters for models where pricing.prompt and pricing.completion are "0".

        Returns:
            List of AvailableModel objects (free models only)
        """
        try:
            url = f"{self.base_url}/models"
            headers = {"Authorization": f"Bearer {self.config.api_key}"}

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Exclude non-text generation models
            exclude_patterns = [
                "diffusion",
                "flux",
                "sdxl",
                "image",
                "audio",
                "whisper",
                "midjourney",
                "dall-e",
                "tts",
            ]

            models = []
            if "data" in data:
                for model in data["data"]:
                    if "id" in model:
                        model_id = model["id"].lower()

                        # Check pricing
                        pricing = model.get("pricing", {})
                        prompt_price = pricing.get("prompt", "0")
                        completion_price = pricing.get("completion", "0")

                        # Convert to float to handle "0", "0.0", "0.000000"
                        try:
                            is_free = float(prompt_price) == 0.0 and float(completion_price) == 0.0
                        except (ValueError, TypeError):
                            is_free = False

                        # Check if excluded
                        is_excluded = any(pattern in model_id for pattern in exclude_patterns)

                        if is_free and not is_excluded:
                            models.append(
                                AvailableModel(
                                    id=model["id"],
                                    name=model.get("name", model["id"]),
                                    description=model.get("description", ""),
                                    context_length=model.get("context_length"),
                                )
                            )

            # Sort models alphabetically by ID
            models.sort(key=lambda model: model.id.lower())

            logger.info(f"Found {len(models)} free text generation models for OpenRouter")
            return models
        except Exception as e:
            logger.error(f"Failed to get OpenRouter models: {str(e)}")
            return []

    def _prepare_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """
        Prepare messages for OpenRouter format (OpenAI-compatible).

        Args:
            messages: List of Message objects

        Returns:
            OpenAI-compatible message format
        """
        openai_messages = []
        for msg in messages:
            openai_messages.append({"role": msg.role, "content": msg.content})
        return openai_messages
