"""
Optimization Integration Module.

This module provides integration helpers to seamlessly integrate
optimization services into the orchestrator and API endpoints.

Features:
    - Automatic semantic caching for LLM calls
    - Backpressure handling for SSE streams
    - Token optimization for prompts and conversations
    - Unified configuration management
"""

from collections.abc import AsyncIterator
from typing import Any, Optional

from langchain_core.messages import BaseMessage
from loguru import logger

from app.core.config import settings
from app.services.optimization.backpressure import BackpressureConfig, get_backpressure_manager
from app.services.optimization.semantic_cache import CacheConfig, get_semantic_cache
from app.services.optimization.token_optimizer import TokenOptimizerConfig, get_token_optimizer


class OptimizationManager:
    """
    Unified manager for all optimization services.

    This class provides a single interface to access and configure
    all optimization features, making integration simple and consistent.

    Example:
        ```python
        optimizer = OptimizationManager()

        # Optimize LLM call with caching and token optimization
        response = await optimizer.optimize_llm_call(
            messages=messages,
            tools=tools,
            llm_invoke=llm.invoke
        )

        # Apply backpressure to SSE stream
        async for event in optimizer.apply_backpressure(events):
            yield event
        ```
    """

    def __init__(
        self,
        enable_caching: bool = True,
        enable_backpressure: bool = True,
        enable_token_optimization: bool = True,
    ):
        """
        Initialize optimization manager.

        Args:
            enable_caching: Enable semantic caching
            enable_backpressure: Enable backpressure handling
            enable_token_optimization: Enable token optimization
        """
        self.enable_caching = enable_caching
        self.enable_backpressure = enable_backpressure
        self.enable_token_optimization = enable_token_optimization

        # Initialize services
        self._init_services()

        logger.info(
            f"Optimization manager initialized: "
            f"caching={enable_caching}, "
            f"backpressure={enable_backpressure}, "
            f"token_opt={enable_token_optimization}"
        )

    def _init_services(self):
        """Initialize optimization services."""
        # Semantic cache
        if self.enable_caching:
            try:
                cache_config = CacheConfig(
                    enabled=True,
                    similarity_threshold=getattr(settings, "CACHE_SIMILARITY_THRESHOLD", 0.95),
                    ttl_seconds=getattr(settings, "CACHE_TTL_SECONDS", 3600),
                    max_cache_size=getattr(settings, "CACHE_MAX_SIZE", 10000),
                    redis_host=getattr(settings, "REDIS_HOST", "localhost"),
                    redis_port=getattr(settings, "REDIS_PORT", 6379),
                    redis_db=2,  # Use DB 2 for cache
                )
                self.cache = get_semantic_cache(cache_config)
                logger.info("✓ Semantic cache initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize semantic cache: {e}")
                self.cache = None
                self.enable_caching = False
        else:
            self.cache = None

        # Backpressure manager
        if self.enable_backpressure:
            try:
                bp_config = BackpressureConfig(
                    enabled=True,
                    batch_size=getattr(settings, "BP_BATCH_SIZE", 10),
                    batch_timeout_ms=getattr(settings, "BP_BATCH_TIMEOUT_MS", 100),
                    max_events_per_second=getattr(settings, "BP_MAX_EVENTS_PER_SEC", 100),
                    compression_threshold_bytes=getattr(settings, "BP_COMPRESSION_THRESHOLD", 1024),
                )
                self.backpressure = get_backpressure_manager(bp_config)
                logger.info("✓ Backpressure manager initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize backpressure manager: {e}")
                self.backpressure = None
                self.enable_backpressure = False
        else:
            self.backpressure = None

        # Token optimizer
        if self.enable_token_optimization:
            try:
                token_config = TokenOptimizerConfig(
                    enabled=True,
                    summarization_threshold=getattr(settings, "TOKEN_SUMMARIZATION_THRESHOLD", 20),
                    max_context_messages=getattr(settings, "TOKEN_MAX_CONTEXT_MESSAGES", 10),
                    dynamic_tool_filtering=getattr(settings, "TOKEN_DYNAMIC_TOOL_FILTERING", True),
                    compress_prompts=getattr(settings, "TOKEN_COMPRESS_PROMPTS", True),
                    track_costs=True,
                )
                self.token_optimizer = get_token_optimizer(token_config)
                logger.info("✓ Token optimizer initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize token optimizer: {e}")
                self.token_optimizer = None
                self.enable_token_optimization = False
        else:
            self.token_optimizer = None

    async def optimize_llm_call(
        self,
        messages: list[BaseMessage],
        tools: Optional[list[Any]] = None,
        llm_invoke: Optional[Any] = None,
        query: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Optimize LLM call with caching and token optimization.

        This method:
        1. Checks semantic cache for similar queries
        2. Optimizes messages and tools to reduce tokens
        3. Calls LLM if cache miss
        4. Caches the response
        5. Tracks token usage and costs

        Args:
            messages: List of messages
            tools: Optional list of tools
            llm_invoke: LLM invoke function
            query: Optional query string for caching
            metadata: Optional metadata

        Returns:
            Dictionary with:
                - response: LLM response string
                - cached: Whether response was cached
                - tokens_saved: Number of tokens saved
                - cost_saved: Cost saved in USD
        """
        result = {
            "response": None,
            "cached": False,
            "tokens_saved": 0,
            "cost_saved": 0.0,
            "optimized_messages": messages,
            "optimized_tools": tools,
        }

        # Extract query for caching
        if not query and messages:
            for msg in reversed(messages):
                if hasattr(msg, "content") and isinstance(msg.content, str):
                    query = msg.content
                    break

        # 1. Check semantic cache
        if self.enable_caching and self.cache and query:
            try:
                cached_response = self.cache.get(query, metadata=metadata)
                if cached_response:
                    result["response"] = cached_response
                    result["cached"] = True
                    logger.info(f"✓ Cache HIT for query: {query[:50]}...")
                    return result
            except Exception as e:
                logger.warning(f"Cache lookup failed: {e}")

        # 2. Optimize tokens
        if self.enable_token_optimization and self.token_optimizer:
            try:
                optimized_messages, optimized_tools = self.token_optimizer.optimize_messages(
                    messages=messages, tools=tools, query=query, llm_invoke=llm_invoke
                )
                result["optimized_messages"] = optimized_messages
                result["optimized_tools"] = optimized_tools

                # Calculate tokens saved
                from app.services.optimization.token_optimizer import TokenCounter

                counter = TokenCounter()
                original_tokens = counter.count_messages_tokens(messages)
                optimized_tokens = counter.count_messages_tokens(optimized_messages)
                result["tokens_saved"] = original_tokens - optimized_tokens

                logger.debug(f"Token optimization: {original_tokens} → {optimized_tokens} tokens")
            except Exception as e:
                logger.warning(f"Token optimization failed: {e}")

        # 3. Call LLM (if provided)
        if llm_invoke:
            try:
                response = llm_invoke(result["optimized_messages"])
                result["response"] = response

                # 4. Cache the response
                if self.enable_caching and self.cache and query:
                    try:
                        self.cache.set(query=query, response=response, metadata=metadata)
                        logger.debug(f"Cached response for query: {query[:50]}...")
                    except Exception as e:
                        logger.warning(f"Failed to cache response: {e}")

                # 5. Track token usage
                if self.enable_token_optimization and self.token_optimizer:
                    try:
                        # Estimate tokens (this would be more accurate with actual token counts from LLM)
                        counter = TokenCounter()
                        input_tokens = counter.count_messages_tokens(result["optimized_messages"])
                        output_tokens = counter.count_tokens(response)

                        self.token_optimizer.track_usage(
                            input_tokens=input_tokens, output_tokens=output_tokens
                        )
                    except Exception as e:
                        logger.warning(f"Failed to track token usage: {e}")

            except Exception as e:
                logger.error(f"LLM invocation failed: {e}")
                raise

        return result

    async def apply_backpressure(
        self, events: AsyncIterator[dict[str, Any]]
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Apply backpressure handling to event stream.

        Args:
            events: Async iterator of events

        Yields:
            Processed events with backpressure applied
        """
        if self.enable_backpressure and self.backpressure:
            try:
                async for event in self.backpressure.process(events):
                    yield event
            except Exception as e:
                logger.error(f"Backpressure processing failed: {e}")
                # Fall back to pass-through
                async for event in events:
                    yield event
        else:
            # Pass through without processing
            async for event in events:
                yield event

    def get_stats(self) -> dict[str, Any]:
        """
        Get statistics from all optimization services.

        Returns:
            Dictionary with stats from all services
        """
        stats = {}

        if self.cache:
            try:
                cache_stats = self.cache.get_stats()
                stats["cache"] = cache_stats.to_dict()
            except Exception as e:
                logger.warning(f"Failed to get cache stats: {e}")
                stats["cache"] = {"error": str(e)}

        if self.backpressure:
            try:
                bp_stats = self.backpressure.get_stats()
                stats["backpressure"] = bp_stats.to_dict()
            except Exception as e:
                logger.warning(f"Failed to get backpressure stats: {e}")
                stats["backpressure"] = {"error": str(e)}

        if self.token_optimizer:
            try:
                token_stats = self.token_optimizer.get_stats()
                stats["token_optimization"] = token_stats.to_dict()
            except Exception as e:
                logger.warning(f"Failed to get token stats: {e}")
                stats["token_optimization"] = {"error": str(e)}

        return stats

    def reset_stats(self):
        """Reset statistics for all services."""
        if self.cache:
            try:
                self.cache.clear()
            except Exception as e:
                logger.warning(f"Failed to reset cache stats: {e}")

        if self.backpressure:
            try:
                self.backpressure.reset_stats()
            except Exception as e:
                logger.warning(f"Failed to reset backpressure stats: {e}")

        if self.token_optimizer:
            try:
                self.token_optimizer.reset_stats()
            except Exception as e:
                logger.warning(f"Failed to reset token stats: {e}")


# Global optimization manager instance
_optimization_manager: Optional[OptimizationManager] = None


def get_optimization_manager() -> OptimizationManager:
    """
    Get or create global optimization manager instance.

    Returns:
        OptimizationManager instance
    """
    global _optimization_manager

    if _optimization_manager is None:
        _optimization_manager = OptimizationManager()

    return _optimization_manager
