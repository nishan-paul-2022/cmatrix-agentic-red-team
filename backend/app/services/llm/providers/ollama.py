"""Ollama LLM provider for local model inference."""

from typing import Any

import requests
from loguru import logger

from app.models.llm import AvailableModel

from .base import LLMProvider, Message, ProviderConfig, StreamingProviderMixin


class OllamaProvider(LLMProvider, StreamingProviderMixin):
    """Ollama provider for local LLM models."""

    def __init__(self, config: ProviderConfig):
        """
        Initialize Ollama provider.

        Args:
            config: Provider configuration with base_url and model
        """
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"

        # Validate configuration - model is optional when just fetching available models
        if not self.config.model:
            logger.warning("No model specified for Ollama provider (OK for fetching models)")

        logger.info(f"🐳 Ollama provider initialized with base_url: {self.base_url}")

    def invoke(self, messages: list[Message], **kwargs) -> str:
        """
        Invoke Ollama model.

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Returns:
            Response text
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.config.model,
            "messages": self._prepare_messages(messages),
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens or 512),
            },
        }

        def make_request():
            response = requests.post(url, json=payload, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()

        result = self._retry_request(make_request)

        # Ollama returns messages, get the last one
        if "message" in result:
            return result["message"]["content"]
        elif "response" in result:  # Some older Ollama versions
            return result["response"]
        else:
            raise ValueError(f"Unexpected response format from Ollama: {result}")

    def invoke_stream(self, messages: list[Message], **kwargs):
        """
        Invoke Ollama model with streaming.

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Yields:
            Response chunks
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.config.model,
            "messages": self._prepare_messages(messages),
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens or 512),
            },
        }

        def make_request():
            response = requests.post(url, json=payload, timeout=self.config.timeout, stream=True)
            response.raise_for_status()
            return response

        response = self._retry_request(make_request)

        try:
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]  # Remove 'data: ' prefix

                    try:
                        chunk = requests.utils.json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            yield chunk["message"]["content"]
                        elif "response" in chunk:  # Older format
                            yield chunk["response"]
                    except requests.utils.json.JSONDecodeError:
                        continue  # Skip non-JSON lines
        except Exception as e:
            logger.error(f"Error in Ollama streaming: {str(e)}")
            raise

    def get_available_models(self) -> list[AvailableModel]:
        """
        Get list of available models from Ollama.

        Returns:
            List of AvailableModel objects
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            models = []
            if "models" in data:
                for model in data["models"]:
                    if "name" in model:
                        models.append(
                            AvailableModel(
                                id=model["name"],
                                name=model["name"],
                                description=f"Ollama - {model['name']}",
                                context_length=None,
                            )
                        )

            # Sort models alphabetically by ID
            models.sort(key=lambda model: model.id.lower())

            return models
        except Exception as e:
            logger.error(f"Failed to get Ollama models: {str(e)}")
            return []

    def _prepare_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """
        Prepare messages for Ollama format.

        Args:
            messages: List of Message objects

        Returns:
            Ollama-compatible message format
        """
        ollama_messages = []
        for msg in messages:
            ollama_messages.append({"role": msg.role, "content": msg.content})
        return ollama_messages
