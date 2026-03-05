"""
Logger configuration module.

Sets up logging for the entire application using loguru.
"""

import sys
from pathlib import Path
from loguru import logger

from configs.config import get_config


def setup_logger(config=None):
    """
    Configure logger for the application.
    
    Args:
        config: Configuration object. If None, uses default config.
    """
    if config is None:
        config = get_config()
    
    # Remove default handler
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stdout,
        level=config.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    
    # File handler
    log_file = config.LOGS_DIR / f"app_{config.LOG_LEVEL}.log"
    logger.add(
        str(log_file),
        level=config.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days",
    )
    
    return logger


# Initialize logger
logger = setup_logger()
