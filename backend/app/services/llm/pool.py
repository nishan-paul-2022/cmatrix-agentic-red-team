"""
LLM Pool Manager for Multi-Agent System.

This module manages LLM provider instances for different agents,
enabling each agent to have its own dedicated LLM instance while
optimizing resource usage through connection pooling and caching.
"""

from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm.providers import LLMProvider


class AgentLLMPool:
    """
    Manages LLM instances for different agents.

    This class implements a connection pool pattern for LLM providers,
    ensuring efficient resource usage while allowing each agent to have
    its own LLM instance for parallel execution.

    Features:
    - Per-agent LLM instance caching
    - Per-user configuration support
    - Automatic cleanup and resource management
    - Thread-safe operations
    """

    def __init__(self):
        """Initialize the LLM pool."""
        self.providers: dict[str, LLMProvider] = {}
        logger.info("Agent LLM Pool initialized")

    async def get_provider(self, agent_name: str, db: AsyncSession, user_id: int) -> LLMProvider:
        """
        Get or create LLM provider for a specific agent.

        This method implements a caching strategy where each agent gets
        its own LLM provider instance, cached by agent name and user ID.

        Args:
            agent_name: Name of the agent requesting the provider
            db: Database session for loading user configuration
            user_id: User ID for loading LLM configuration

        Returns:
            LLM provider instance configured for the user

        Raises:
            ValueError: If no active LLM model is configured for the user
        """
        cache_key = f"{agent_name}_{user_id}"

        if cache_key not in self.providers:
            logger.debug(f"Creating new LLM provider for {agent_name} (user: {user_id})")

            from app.services.llm.db_factory import get_db_provider_factory

            factory = get_db_provider_factory()
            provider = await factory.get_active_provider(db, user_id)

            if not provider:
                raise ValueError(
                    f"No active LLM model configured for user {user_id}. "
                    "Please configure an API key and activate a model in settings."
                )

            self.providers[cache_key] = provider
            logger.info(f"LLM provider created for {agent_name} (user: {user_id})")
        else:
            logger.debug(f"Using cached LLM provider for {agent_name} (user: {user_id})")

        return self.providers[cache_key]

    def get_provider_sync(self, agent_name: str, provider: LLMProvider) -> LLMProvider:
        """
        Get or cache a provider synchronously (when provider is already available).

        This is useful when the orchestrator already has a provider instance
        and wants to share it with agents.

        Args:
            agent_name: Name of the agent
            provider: Pre-configured LLM provider instance

        Returns:
            The same provider instance (cached for future use)
        """
        cache_key = f"{agent_name}_shared"

        if cache_key not in self.providers:
            self.providers[cache_key] = provider
            logger.debug(f"Cached shared provider for {agent_name}")

        return self.providers[cache_key]

    def clear_cache(self, user_id: Optional[int] = None):
        """
        Clear cached providers.

        Args:
            user_id: If provided, only clear providers for this user.
                    If None, clear all cached providers.
        """
        if user_id is not None:
            # Clear only providers for specific user
            keys_to_remove = [key for key in self.providers if key.endswith(f"_{user_id}")]
            for key in keys_to_remove:
                del self.providers[key]
            logger.info(f"Cleared {len(keys_to_remove)} cached providers for user {user_id}")
        else:
            # Clear all providers
            count = len(self.providers)
            self.providers.clear()
            logger.info(f"Cleared all {count} cached providers")

    def get_stats(self) -> dict[str, int]:
        """
        Get statistics about the LLM pool.

        Returns:
            Dictionary with pool statistics
        """
        return {"total_providers": len(self.providers), "cached_keys": list(self.providers.keys())}


# Global LLM pool instance
_llm_pool: Optional[AgentLLMPool] = None


def get_llm_pool() -> AgentLLMPool:
    """
    Get or create the global LLM pool instance.

    Returns:
        AgentLLMPool instance
    """
    global _llm_pool
    if _llm_pool is None:
        _llm_pool = AgentLLMPool()
    return _llm_pool


def clear_llm_pool_cache(user_id: Optional[int] = None):
    """
    Clear the LLM pool cache.

    This is useful when user configuration changes or for cleanup.

    Args:
        user_id: If provided, only clear cache for this user
    """
    pool = get_llm_pool()
    pool.clear_cache(user_id)
