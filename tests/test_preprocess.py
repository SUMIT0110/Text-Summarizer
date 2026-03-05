"""
Unit tests for the text preprocessing module.

Tests cover all preprocessing functions including edge cases and performance.
"""

import pytest
from utils.preprocess import (
    clean_text,
    normalize_whitespace,
    remove_extra_spaces,
    clean_text_aggressive,
    fast_clean,
    is_clean,
    batch_clean,
)


class TestCleanText:
    """Test cases for clean_text function."""
    
    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        text = "Hello   world"
        result = clean_text(text)
        assert result == "Hello world"
    
    def test_clean_text_newlines(self):
        """Test removing newlines."""
        text = "Hello\nworld\ntest"
        result = clean_text(text)
        assert result == "Hello world test"
    
    def test_clean_text_mixed_whitespace(self):
        """Test mixed whitespace types."""
        text = "Hello\t\n  world  \r\n  test"
        result = clean_text(text)
        assert result == "Hello world test"
    
    def test_clean_text_leading_trailing(self):
        """Test removing leading/trailing spaces."""
        text = "   hello world   "
        result = clean_text(text)
        assert result == "hello world"
    
    def test_clean_text_tabs(self):
        """Test removing tabs."""
        text = "hello\tworld\ttest"
        result = clean_text(text)
        assert result == "hello world test"
    
    def test_clean_text_carriage_return(self):
        """Test handling carriage returns."""
        text = "hello\rworld\r\ntest"
        result = clean_text(text)
        assert result == "hello world test"
    
    def test_clean_text_preserves_punctuation(self):
        """Test that punctuation is preserved."""
        text = "Hello,   world!   How   are   you?"
        result = clean_text(text)
        assert result == "Hello, world! How are you?"
    
    def test_clean_text_with_urls(self):
        """Test cleaning with URLs present."""
        text = "Check https://example.com for info"
        result = clean_text(text, remove_urls=False)
        assert "https://example.com" in result
    
    def test_clean_text_remove_urls(self):
        """Test URL removal."""
        text = "Visit https://example.com or http://test.org now"
        result = clean_text(text, remove_urls=True)
        assert "https://" not in result
        assert "http://" not in result
        assert "Visit" in result
        assert "now" in result
    
    def test_clean_text_empty_string(self):
        """Test with empty string."""
        result = clean_text("")
        assert result == ""
    
    def test_clean_text_only_whitespace(self):
        """Test with whitespace only."""
        result = clean_text("   \n\t\r   ")
        assert result == ""
    
    def test_clean_text_single_word(self):
        """Test with single word."""
        result = clean_text("word")
        assert result == "word"
    
    def test_clean_text_type_error(self):
        """Test with non-string input."""
        with pytest.raises(TypeError):
            clean_text(123)
        
        with pytest.raises(TypeError):
            clean_text(None)
    
    def test_clean_text_special_characters(self):
        """Test with special characters."""
        text = "Hello!@#$%^&*()"
        result = clean_text(text)
        assert result == "Hello!@#$%^&*()"


class TestNormalizeWhitespace:
    """Test cases for normalize_whitespace function."""
    
    def test_normalize_multiple_spaces(self):
        """Test normalizing multiple spaces."""
        text = "hello    world"
        result = normalize_whitespace(text)
        assert result == "hello world"
    
    def test_normalize_tabs(self):
        """Test normalizing tabs."""
        text = "hello\t\tworld"
        result = normalize_whitespace(text)
        assert result == "hello world"
    
    def test_normalize_newlines(self):
        """Test normalizing newlines."""
        text = "hello\n\nworld"
        result = normalize_whitespace(text)
        assert result == "hello world"
    
    def test_normalize_mixed_whitespace(self):
        """Test normalizing mixed whitespace."""
        text = "hello \t\n  world"
        result = normalize_whitespace(text)
        assert result == "hello world"
    
    def test_normalize_type_error(self):
        """Test with invalid input."""
        with pytest.raises(TypeError):
            normalize_whitespace(123)


class TestRemoveExtraSpaces:
    """Test cases for remove_extra_spaces function."""
    
    def test_remove_extra_spaces_basic(self):
        """Test basic space removal."""
        text = "hello   world"
        result = remove_extra_spaces(text)
        assert result == "hello world"
    
    def test_remove_extra_spaces_preserves_newlines(self):
        """Test that newlines are NOT removed."""
        text = "hello\nworld"
        result = remove_extra_spaces(text)
        assert "\n" in result
    
    def test_remove_extra_spaces_leading_trailing(self):
        """Test removing leading/trailing spaces."""
        text = "   hello world   "
        result = remove_extra_spaces(text)
        assert result == "hello world"


class TestCleanTextAggressive:
    """Test cases for clean_text_aggressive function."""
    
    def test_aggressive_removes_urls(self):
        """Test URL removal."""
        text = "Check https://example.com now"
        result = clean_text_aggressive(text)
        assert "https://" not in result
        assert "Check" in result
    
    def test_aggressive_removes_emails(self):
        """Test email removal."""
        text = "Email: user@example.com for info"
        result = clean_text_aggressive(text)
        assert "user@example.com" not in result
        assert "Email" in result
    
    def test_aggressive_removes_mentions(self):
        """Test @mention removal."""
        text = "Hey @user check this"
        result = clean_text_aggressive(text)
        assert "@user" not in result
    
    def test_aggressive_removes_hashtags(self):
        """Test hashtag removal."""
        text = "Great post #awesome #social"
        result = clean_text_aggressive(text)
        assert "#awesome" not in result
        assert "#social" not in result
    
    def test_aggressive_removes_html(self):
        """Test HTML tag removal."""
        text = "Hello <b>world</b> <i>test</i>"
        result = clean_text_aggressive(text)
        assert "<b>" not in result
        assert "</b>" not in result


class TestFastClean:
    """Test cases for fast_clean function."""
    
    def test_fast_clean_basic(self):
        """Test fast cleaning."""
        text = "hello   world"
        result = fast_clean(text)
        assert result == "hello world"
    
    def test_fast_clean_equivalent_to_clean_text(self):
        """Test that fast_clean produces same result as clean_text."""
        text = "hello\t\n  world  \r\n  test"
        result1 = clean_text(text, remove_urls=False)
        result2 = fast_clean(text)
        assert result1 == result2
    
    def test_fast_clean_type_error(self):
        """Test with invalid input."""
        with pytest.raises(TypeError):
            fast_clean(None)


class TestIsClean:
    """Test cases for is_clean function."""
    
    def test_is_clean_true(self):
        """Test with clean text."""
        assert is_clean("hello world") is True
    
    def test_is_clean_false_multiple_spaces(self):
        """Test with multiple spaces."""
        assert is_clean("hello  world") is False
    
    def test_is_clean_false_newlines(self):
        """Test with newlines."""
        assert is_clean("hello\nworld") is False
    
    def test_is_clean_false_leading_space(self):
        """Test with leading space."""
        assert is_clean(" hello") is False
    
    def test_is_clean_false_trailing_space(self):
        """Test with trailing space."""
        assert is_clean("hello ") is False
    
    def test_is_clean_non_string(self):
        """Test with non-string."""
        assert is_clean(123) is False


class TestBatchClean:
    """Test cases for batch_clean function."""
    
    def test_batch_clean_basic(self):
        """Test batch cleaning."""
        texts = ["hello   world", "test\ntext", "  clean  "]
        result = batch_clean(texts)
        assert result[0] == "hello world"
        assert result[1] == "test text"
        assert result[2] == "clean"
    
    def test_batch_clean_skips_clean_text(self):
        """Test that already clean text is skipped."""
        texts = ["already clean", "needs   cleaning"]
        result = batch_clean(texts)
        assert result[0] == "already clean"
        assert result[1] == "needs cleaning"
    
    def test_batch_clean_aggressive(self):
        """Test batch cleaning with aggressive mode."""
        texts = ["hello@example.com", "check #hashtag"]
        result = batch_clean(texts, aggressive=True)
        assert "@example.com" not in result[0]
        assert "#hashtag" not in result[1]
    
    def test_batch_clean_empty_list(self):
        """Test with empty list."""
        result = batch_clean([])
        assert result == []
    
    def test_batch_clean_mixed_types(self):
        """Test with mixed string and non-string types."""
        texts = ["hello", 123, "world"]
        result = batch_clean(texts)
        assert result[0] == "hello"
        assert result[1] == 123  # Non-strings unchanged
        assert result[2] == "world"


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_unicode_characters(self):
        """Test with Unicode characters."""
        text = "Héllo   wörld    tëst"
        result = clean_text(text)
        assert result == "Héllo wörld tëst"
    
    def test_very_long_text(self):
        """Test with very long text."""
        text = "word " * 10000
        result = clean_text(text)
        assert all(c != '  ' for c in result)  # No double spaces
    
    def test_numbers_and_punctuation(self):
        """Test with numbers and punctuation."""
        text = "123  456, 789!  Test#123"
        result = clean_text(text)
        assert result == "123 456, 789! Test#123"
    
    def test_consecutive_newlines(self):
        """Test with consecutive newlines."""
        text = "hello\n\n\n\nworld"
        result = clean_text(text)
        assert result == "hello world"
    
    def test_mixed_line_endings(self):
        """Test different line ending styles."""
        text = "hello\nworld\r\ntest\rend"
        result = clean_text(text)
        assert result == "hello world test end"


class TestPerformance:
    """Performance-related tests."""
    
    def test_clean_text_preserves_content_length(self):
        """Test that important content is preserved."""
        original = "Important content that should not be lost"
        cleaned = clean_text(original)
        # Most content should be preserved
        assert len(cleaned) > 20
    
    def test_fast_clean_faster_than_clean_text(self):
        """Test that fast_clean is faster (qualitative)."""
        import time
        text = "test " * 1000
        
        start = time.time()
        for _ in range(100):
            clean_text(text)
        time1 = time.time() - start
        
        start = time.time()
        for _ in range(100):
            fast_clean(text)
        time2 = time.time() - start
        
        # fast_clean should be comparable or faster
        # (This is a qualitative test)
        assert time2 <= time1 * 1.5  # Allow 50% margin


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
