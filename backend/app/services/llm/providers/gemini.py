"""Google Gemini LLM provider."""

import google.generativeai as genai
from loguru import logger

from app.models.llm import AvailableModel

from .base import LLMProvider, Message, ProviderConfig, StreamingProviderMixin


class GeminiProvider(LLMProvider, StreamingProviderMixin):
    """Google Gemini provider for Gemini models."""

    def __init__(self, config: ProviderConfig):
        """
        Initialize Gemini provider.

        Args:
            config: Provider configuration with API key and model
        """
        super().__init__(config)

        # Validate configuration
        if not self.config.api_key:
            raise ValueError("API key must be specified for Gemini provider")

        # Model is optional when just fetching available models
        if not self.config.model:
            logger.warning("No model specified for Gemini provider (OK for fetching models)")
            # Initialize without a specific model
            genai.configure(api_key=self.config.api_key)
            self.client = None
        else:
            # Initialize Gemini client with model
            genai.configure(api_key=self.config.api_key)
            self.client = genai.GenerativeModel(self.config.model)

        logger.info(f"🤖 Gemini provider initialized with model: {self.config.model}")

    def invoke(self, messages: list[Message], **kwargs) -> str:
        """
        Invoke Gemini model.

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Returns:
            Response text
        """
        try:
            # Convert messages to Gemini format
            gemini_messages = self._prepare_messages(messages)

            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=kwargs.get("temperature", self.config.temperature),
                max_output_tokens=kwargs.get("max_tokens", self.config.max_tokens or 512),
            )

            # Generate response
            response = self.client.generate_content(
                gemini_messages, generation_config=generation_config
            )

            return response.text

        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise

    def invoke_stream(self, messages: list[Message], **kwargs):
        """
        Invoke Gemini model with streaming.

        Args:
            messages: List of chat messages
            **kwargs: Additional parameters

        Yields:
            Response chunks
        """
        try:
            # Convert messages to Gemini format
            gemini_messages = self._prepare_messages(messages)

            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=kwargs.get("temperature", self.config.temperature),
                max_output_tokens=kwargs.get("max_tokens", self.config.max_tokens or 512),
            )

            # Generate streaming response
            response = self.client.generate_content(
                gemini_messages, generation_config=generation_config, stream=True
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Error in Gemini streaming: {str(e)}")
            raise

    def get_available_models(self) -> list[AvailableModel]:
        """
        Get list of available models from Gemini.

        Returns:
            List of AvailableModel objects (stable text generation models only)
        """
        try:
            models = genai.list_models()
            available_models = []

            for model in models:
                model_name = model.name.replace("models/", "").lower()

                # Exclusion patterns for non-text-generation or unstable models
                exclude_patterns = [
                    "image",  # Image generation models (e.g., gemini-2.5-flash-image)
                    "imagen",  # Imagen models
                    "embedding",  # Embedding models
                    "vision",  # Vision-only models
                    "-exp-",  # Experimental models (e.g., gemini-1.5-pro-exp-0801)
                    "-exp",  # Experimental models (e.g., gemini-2.0-flash-exp)
                    "preview",  # Preview models
                    "deprecated",  # Deprecated models
                    "banana",  # Nano Banana (image generation codename)
                    "aqa",  # Attributed Question Answering models
                    "001",  # Exclude older 001 versions
                    "lite",  # Exclude lite models
                ]

                # Check if model name contains any exclusion pattern
                should_exclude = any(pattern in model_name for pattern in exclude_patterns)

                # Filter for stable text generation models only
                # Include models that:
                # 1. Support 'generateContent' (text generation capability)
                # 2. Do NOT support 'embedContent' (not embedding models)
                # 3. Do NOT match any exclusion patterns
                if (
                    "generateContent" in model.supported_generation_methods
                    and "embedContent" not in model.supported_generation_methods
                    and not should_exclude
                ):
                    # Use original model name (with proper casing) for the ID
                    original_name = model.name.replace("models/", "")
                    available_models.append(
                        AvailableModel(
                            id=original_name,
                            name=model.display_name or original_name,
                            description=model.description,
                            context_length=model.input_token_limit,
                        )
                    )

            # Sort models alphabetically by ID
            available_models.sort(key=lambda model: model.id.lower())

            logger.info(f"Found {len(available_models)} stable text generation models for Gemini")
            return available_models
        except Exception as e:
            logger.error(f"Failed to get Gemini models: {str(e)}")
            return []

    def _prepare_messages(self, messages: list[Message]) -> str:
        """
        Prepare messages for Gemini format.

        Gemini uses a simple text/string format for prompts, not structured messages like OpenAI.

        Args:
            messages: List of Message objects

        Returns:
            Formatted prompt string
        """
        prompt_parts = []

        for msg in messages:
            if msg.role == "system":
                # Gemini doesn't have explicit system messages, so we'll include them as context
                prompt_parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")

        # Join all parts with newlines
        return "\n\n".join(prompt_parts)
