"""Logging configuration for the application."""

import logging
import sys

from typing import Optional
from loguru import logger

from app.core.config import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure application logging using loguru.
    
    Args:
        log_level: Override default log level from settings
    """
    # Remove default handler
    logger.remove()
    
    # Get log level
    level = log_level or settings.LOG_LEVEL
    
    # Console handler with colorization
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )
    
    logger.info(f"Logging configured with level: {level}")



