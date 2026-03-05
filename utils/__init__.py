"""
Utils package initialization.
"""

from utils.text_processor import TextProcessor
from utils.logger import logger, setup_logger
from utils.preprocess import (
    clean_text,
    normalize_whitespace,
    remove_extra_spaces,
    clean_text_aggressive,
    fast_clean,
    is_clean,
    batch_clean,
)

__all__ = [
    "TextProcessor",
    "logger",
    "setup_logger",
    "clean_text",
    "normalize_whitespace",
    "remove_extra_spaces",
    "clean_text_aggressive",
    "fast_clean",
    "is_clean",
    "batch_clean",
]
