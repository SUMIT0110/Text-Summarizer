"""
Text preprocessing and processing utilities.

Handles text cleaning, tokenization, and validation.
"""

import re
from typing import List, Tuple
from utils.logger import logger


class TextProcessor:
    """Text processing utilities for summarization."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text to clean.
        
        Returns:
            Cleaned text.
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text)}")
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\']', '', text)
        
        # Remove multiple punctuation
        text = re.sub(r'([.!?]){2,}', r'\1', text)
        
        return text
    
    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Text to split.
        
        Returns:
            List of sentences.
        """
        # Simple sentence splitting on common delimiters
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def validate_text(
        text: str,
        min_length: int = 10,
        max_length: int = 1024
    ) -> Tuple[bool, str]:
        """
        Validate text for summarization.
        
        Args:
            text: Text to validate.
            min_length: Minimum required text length.
            max_length: Maximum allowed text length.
        
        Returns:
            Tuple of (is_valid, message).
        """
        if not isinstance(text, str):
            return False, "Input must be a string"
        
        text = text.strip()
        
        if len(text) < min_length:
            return False, f"Text too short. Minimum {min_length} characters required."
        
        if len(text) > max_length:
            return False, f"Text too long. Maximum {max_length} characters allowed."
        
        if len(text.split()) < 3:
            return False, "Text must contain at least 3 words."
        
        return True, "Text is valid"
    
    @staticmethod
    def preprocess(
        text: str,
        min_length: int = 10,
        max_length: int = 1024
    ) -> str:
        """
        End-to-end preprocessing pipeline.
        
        Args:
            text: Text to preprocess.
            min_length: Minimum required text length.
            max_length: Maximum allowed text length.
        
        Returns:
            Preprocessed text.
        
        Raises:
            ValueError: If text validation fails.
        """
        # Validate input
        is_valid, message = TextProcessor.validate_text(
            text, min_length, max_length
        )
        if not is_valid:
            raise ValueError(message)
        
        # Clean text
        cleaned = TextProcessor.clean_text(text)
        
        logger.debug(f"Text preprocessed. Original length: {len(text)}, Cleaned length: {len(cleaned)}")
        
        return cleaned
    
    @staticmethod
    def count_words(text: str) -> int:
        """
        Count words in text.
        
        Args:
            text: Text to count.
        
        Returns:
            Number of words.
        """
        return len(text.split())
    
    @staticmethod
    def get_text_stats(text: str) -> dict:
        """
        Get statistics about the text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Dictionary with text statistics.
        """
        sentences = TextProcessor.split_into_sentences(text)
        words = text.split()
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        }
