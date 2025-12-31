"""
Optimization API Endpoints.

This module provides REST API endpoints for monitoring and controlling
optimization services.

Endpoints:
    GET  /api/v1/optimization/stats - Get optimization statistics
    POST /api/v1/optimization/reset - Reset statistics
    GET  /api/v1/optimization/cache/stats - Get cache statistics
    POST /api/v1/optimization/cache/clear - Clear cache
    GET  /api/v1/optimization/config - Get optimization configuration
    POST /api/v1/optimization/config - Update optimization configuration
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel, Field

from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.optimization.integration import get_optimization_manager

router = APIRouter(prefix="/optimization", tags=["optimization"])


class OptimizationConfigUpdate(BaseModel):
    """Model for updating optimization configuration."""

    enable_caching: bool | None = Field(None, description="Enable/disable semantic caching")
    enable_backpressure: bool | None = Field(
        None, description="Enable/disable backpressure handling"
    )
    enable_token_optimization: bool | None = Field(
        None, description="Enable/disable token optimization"
    )
    cache_similarity_threshold: float | None = Field(
        None, ge=0.0, le=1.0, description="Cache similarity threshold (0.0-1.0)"
    )
    cache_ttl_seconds: int | None = Field(None, gt=0, description="Cache TTL in seconds")


class OptimizationStats(BaseModel):
    """Model for optimization statistics response."""

    cache: dict[str, Any] | None = None
    backpressure: dict[str, Any] | None = None
    token_optimization: dict[str, Any] | None = None
    summary: dict[str, Any]


@router.get(
    "/stats",
    response_model=OptimizationStats,
    summary="Get optimization statistics",
    description="Retrieve statistics from all optimization services including cache hit rates, token savings, and backpressure metrics",
)
async def get_optimization_stats(
    current_user: User = Depends(get_current_user),
) -> OptimizationStats:
    """
    Get optimization statistics.

    Returns comprehensive statistics from all optimization services:
    - Semantic cache: hit rate, cost savings, response times
    - Backpressure: event throughput, compression ratios
    - Token optimization: tokens saved, cost reduction

    Args:
        current_user: Authenticated user

    Returns:
        Optimization statistics
    """
    try:
        optimizer = get_optimization_manager()
        stats = optimizer.get_stats()

        # Calculate summary metrics
        summary = {
            "total_cost_saved_usd": 0.0,
            "total_requests": 0,
            "optimization_enabled": {
                "caching": optimizer.enable_caching,
                "backpressure": optimizer.enable_backpressure,
                "token_optimization": optimizer.enable_token_optimization,
            },
        }

        # Aggregate cost savings
        if "cache" in stats and "cost_savings_usd" in stats["cache"]:
            summary["total_cost_saved_usd"] += stats["cache"]["cost_savings_usd"]

        if "token_optimization" in stats and "cost_saved_usd" in stats["token_optimization"]:
            summary["total_cost_saved_usd"] += stats["token_optimization"]["cost_saved_usd"]

        # Aggregate request counts
        if "cache" in stats and "total_requests" in stats["cache"]:
            summary["total_requests"] = stats["cache"]["total_requests"]

        return OptimizationStats(
            cache=stats.get("cache"),
            backpressure=stats.get("backpressure"),
            token_optimization=stats.get("token_optimization"),
            summary=summary,
        )

    except Exception as e:
        logger.error(f"Failed to get optimization stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve optimization statistics: {str(e)}",
        )


@router.post(
    "/reset",
    summary="Reset optimization statistics",
    description="Reset all optimization statistics and clear caches",
)
async def reset_optimization_stats(
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """
    Reset optimization statistics.

    This endpoint:
    - Clears all cached entries
    - Resets performance statistics
    - Resets cost tracking

    Args:
        current_user: Authenticated user

    Returns:
        Success message
    """
    try:
        optimizer = get_optimization_manager()
        optimizer.reset_stats()

        logger.info(f"Optimization stats reset by user {current_user.username}")

        return {"message": "Optimization statistics reset successfully", "status": "success"}

    except Exception as e:
        logger.error(f"Failed to reset optimization stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset optimization statistics: {str(e)}",
        )


@router.get(
    "/cache/stats",
    summary="Get cache statistics",
    description="Get detailed semantic cache statistics",
)
async def get_cache_stats(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    """
    Get semantic cache statistics.

    Returns detailed cache performance metrics:
    - Hit rate
    - Total entries
    - Average similarity scores
    - Cost savings

    Args:
        current_user: Authenticated user

    Returns:
        Cache statistics
    """
    try:
        optimizer = get_optimization_manager()

        if not optimizer.cache:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Semantic cache is not enabled",
            )

        stats = optimizer.cache.get_stats()
        return stats.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve cache statistics: {str(e)}",
        )


@router.post(
    "/cache/clear", summary="Clear semantic cache", description="Clear all cached LLM responses"
)
async def clear_cache(current_user: User = Depends(get_current_user)) -> dict[str, str]:
    """
    Clear semantic cache.

    Removes all cached LLM responses. This is useful when:
    - Model has been updated
    - Cached responses are stale
    - Testing cache performance

    Args:
        current_user: Authenticated user

    Returns:
        Success message
    """
    try:
        optimizer = get_optimization_manager()

        if not optimizer.cache:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Semantic cache is not enabled",
            )

        optimizer.cache.clear()

        logger.info(f"Cache cleared by user {current_user.username}")

        return {"message": "Cache cleared successfully", "status": "success"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}",
        )


@router.get(
    "/config",
    summary="Get optimization configuration",
    description="Get current optimization configuration",
)
async def get_optimization_config(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    """
    Get optimization configuration.

    Returns current configuration for all optimization services.

    Args:
        current_user: Authenticated user

    Returns:
        Optimization configuration
    """
    try:
        optimizer = get_optimization_manager()

        config = {
            "caching": {
                "enabled": optimizer.enable_caching,
                "similarity_threshold": optimizer.cache.config.similarity_threshold
                if optimizer.cache
                else None,
                "ttl_seconds": optimizer.cache.config.ttl_seconds if optimizer.cache else None,
                "max_cache_size": optimizer.cache.config.max_cache_size
                if optimizer.cache
                else None,
            },
            "backpressure": {
                "enabled": optimizer.enable_backpressure,
                "batch_size": optimizer.backpressure.config.batch_size
                if optimizer.backpressure
                else None,
                "max_events_per_second": optimizer.backpressure.config.max_events_per_second
                if optimizer.backpressure
                else None,
            },
            "token_optimization": {
                "enabled": optimizer.enable_token_optimization,
                "summarization_threshold": optimizer.token_optimizer.config.summarization_threshold
                if optimizer.token_optimizer
                else None,
                "max_context_messages": optimizer.token_optimizer.config.max_context_messages
                if optimizer.token_optimizer
                else None,
                "dynamic_tool_filtering": optimizer.token_optimizer.config.dynamic_tool_filtering
                if optimizer.token_optimizer
                else None,
            },
        }

        return config

    except Exception as e:
        logger.error(f"Failed to get optimization config: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve optimization configuration: {str(e)}",
        )


@router.get(
    "/health",
    summary="Check optimization services health",
    description="Check if all optimization services are running properly",
)
async def check_optimization_health() -> dict[str, Any]:
    """
    Check optimization services health.

    Returns health status for all optimization services.

    Returns:
        Health status
    """
    try:
        optimizer = get_optimization_manager()

        health = {
            "status": "healthy",
            "services": {
                "cache": {
                    "enabled": optimizer.enable_caching,
                    "healthy": optimizer.cache is not None,
                },
                "backpressure": {
                    "enabled": optimizer.enable_backpressure,
                    "healthy": optimizer.backpressure is not None,
                },
                "token_optimization": {
                    "enabled": optimizer.enable_token_optimization,
                    "healthy": optimizer.token_optimizer is not None,
                },
            },
        }

        # Check if any service is unhealthy
        unhealthy_services = [
            name
            for name, service in health["services"].items()
            if service["enabled"] and not service["healthy"]
        ]

        if unhealthy_services:
            health["status"] = "degraded"
            health["unhealthy_services"] = unhealthy_services

        return health

    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return {"status": "unhealthy", "error": str(e)}
