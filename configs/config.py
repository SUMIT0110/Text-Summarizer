"""
Configuration module for the Text Summarization application.

Centralized settings management for model configuration, hyperparameters,
and application-wide constants.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Base configuration class."""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    MODELS_DIR = PROJECT_ROOT / "models" / "checkpoints"
    DATA_DIR = PROJECT_ROOT / "data"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    # Create directories if they don't exist
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Model configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "facebook/bart-large-cnn")
    DEVICE = os.getenv("DEVICE", "cuda")  # cuda or cpu
    MAX_LENGTH = int(os.getenv("MAX_LENGTH", 150))
    MIN_LENGTH = int(os.getenv("MIN_LENGTH", 30))
    
    # Text processing
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", 1024))
    MIN_INPUT_LENGTH = int(os.getenv("MIN_INPUT_LENGTH", 10))
    
    # Model inference
    NUM_BEAMS = int(os.getenv("NUM_BEAMS", 4))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    EARLY_STOPPING = os.getenv("EARLY_STOPPING", "true").lower() == "true"
    
    # Application settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Cache settings
    CACHE_MODELS = os.getenv("CACHE_MODELS", "true").lower() == "true"
    MODEL_CACHE_DIR = MODELS_DIR / "huggingface_cache"


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    MODEL_NAME = "t5-small"  # Lighter model for tests
    NUM_BEAMS = 2


def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration based on environment.
    
    Args:
        env: Environment name ('development', 'production', 'testing').
             If None, uses ENVIRONMENT variable or defaults to 'development'.
    
    Returns:
        Config: Configuration object for the specified environment.
    """
    if env is None:
        env = os.getenv("ENVIRONMENT", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()
