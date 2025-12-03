"""Cerebras LLM provider."""

from typing import Any

import requests
from loguru import logger

from app.models.llm import AvailableModel

from .base import LLMProvider, Message, ProviderConfig, StreamingProviderMixin


class CerebrasProvider(LLMProvider, StreamingProviderMixin):
    """Cerebras provider for various LLM models."""

    def __init__(self, config: ProviderConfig):
        """
        Initialize Cerebras provider.

        Args:
            config: Provider configuration with API key and model
        """
        super().__init__(config)
        self.base_url = "https://api.cerebras.ai/v1"  # Assuming standard Cerebras API endpoint

        # Validate configuration
        if not self.config.api_key:
            raise ValueError("API key must be specified for Cerebras provider")

        # Model is optional when just fetching available models
        if not self.config.model:
            logger.warning("No model specified for Cerebras provider (OK for fetching models)")

        logger.info(f"🧠 Cerebras provider initialized with model: {self.config.model}")

    def invoke(self, messages: list[Message], **kwargs) -> str:
        """
        Invoke Cerebras model.

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
            raise ValueError(f"Unexpected response format from Cerebras: {result}")

    def invoke_stream(self, messages: list[Message], **kwargs):
        """
        Invoke Cerebras model with streaming.

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
            logger.error(f"Error in Cerebras streaming: {str(e)}")
            raise

    def get_available_models(self) -> list[AvailableModel]:
        """
        Get list of available models from Cerebras.

        Returns:
            List of AvailableModel objects
        """
        try:
            url = f"{self.base_url}/models"
            headers = {"Authorization": f"Bearer {self.config.api_key}"}

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            models = []
            if "data" in data:
                for model in data["data"]:
                    if "id" in model:
                        models.append(
                            AvailableModel(
                                id=model["id"],
                                name=model["id"],
                                description=f"Cerebras - {model['id']}",
                                context_length=model.get("context_length"),
                            )
                        )

            # Sort models alphabetically by ID
            models.sort(key=lambda model: model.id.lower())

            return models
        except Exception as e:
            logger.error(f"Failed to get Cerebras models: {str(e)}")
            return []

    def _prepare_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """
        Prepare messages for Cerebras format (OpenAI-compatible).

        Args:
            messages: List of Message objects

        Returns:
            OpenAI-compatible message format
        """
        prepared_messages = []
        for msg in messages:
            prepared_messages.append({"role": msg.role, "content": msg.content})
        return prepared_messages
