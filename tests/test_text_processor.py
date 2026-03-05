"""
Unit tests for text processing module.

Tests cover text cleaning, validation, and preprocessing functionality.
"""

import pytest
from utils.text_processor import TextProcessor


class TestTextProcessor:
    """Test cases for TextProcessor class."""
    
    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        text = "This   is  a   test"
        result = TextProcessor.clean_text(text)
        assert result == "This is a test"
    
    def test_clean_text_special_chars(self):
        """Test cleaning special characters."""
        text = "Hello@#$%World!"
        result = TextProcessor.clean_text(text)
        assert "@#$%" not in result
    
    def test_split_into_sentences(self):
        """Test sentence splitting."""
        text = "This is first sentence. This is second sentence! Third one?"
        sentences = TextProcessor.split_into_sentences(text)
        assert len(sentences) == 3
    
    def test_validate_text_valid(self):
        """Test validation with valid text."""
        text = "This is a valid text for summarization."
        is_valid, message = TextProcessor.validate_text(text)
        assert is_valid is True
    
    def test_validate_text_too_short(self):
        """Test validation with text too short."""
        text = "Short"
        is_valid, message = TextProcessor.validate_text(text)
        assert is_valid is False
        assert "too short" in message.lower()
    
    def test_validate_text_too_long(self):
        """Test validation with text exceeding max length."""
        text = "a" * 1100
        is_valid, message = TextProcessor.validate_text(text, max_length=1024)
        assert is_valid is False
        assert "too long" in message.lower()
    
    def test_validate_text_not_string(self):
        """Test validation with non-string input."""
        is_valid, message = TextProcessor.validate_text(123)
        assert is_valid is False
    
    def test_preprocess_valid_text(self):
        """Test full preprocessing pipeline."""
        text = "This   is   a   test   text   for   summarization."
        result = TextProcessor.preprocess(text)
        assert len(result) > 0
        assert result.strip() == result  # No leading/trailing whitespace
    
    def test_preprocess_invalid_text(self):
        """Test preprocessing with invalid text."""
        with pytest.raises(ValueError):
            TextProcessor.preprocess("Short")
    
    def test_count_words(self):
        """Test word counting."""
        text = "This is a test with five words"
        count = TextProcessor.count_words(text)
        assert count == 6
    
    def test_get_text_stats(self):
        """Test text statistics generation."""
        text = "This is a test. Another sentence here."
        stats = TextProcessor.get_text_stats(text)
        
        assert "character_count" in stats
        assert "word_count" in stats
        assert "sentence_count" in stats
        assert "avg_sentence_length" in stats
        assert "avg_word_length" in stats
        
        assert stats["word_count"] == 7
        assert stats["sentence_count"] == 2
    
    def test_get_text_stats_empty_text(self):
        """Test text statistics with empty text."""
        text = ""
        stats = TextProcessor.get_text_stats(text)
        assert stats["word_count"] == 0
        assert stats["sentence_count"] == 0
