"""
Text Summarization Model Module.

Handles model loading, inference, and summarization logic using BART transformer.
Implements efficient chunk-based processing for long documents with deterministic output.
"""

import os
import warnings
import torch
import re
from typing import List, Tuple, Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Suppress deprecation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning)

from utils.logger import logger


# Global model state - loaded once for entire application lifecycle
_model = None
_tokenizer = None
_device = None


class SummarizationError(Exception):
    """Custom exception for summarization errors."""
    pass


def _initialize_model(model_name: str = "facebook/bart-large-cnn") -> Tuple:
    """
    Initialize the transformer model and tokenizer once.
    
    Uses global variables to ensure the model is loaded only once
    for better performance and memory efficiency.
    
    Args:
        model_name: HuggingFace model identifier.
    
    Returns:
        Tuple of (model, tokenizer, device).
    
    Raises:
        SummarizationError: If model loading fails.
    """
    global _model, _tokenizer, _device
    
    if _model is not None:
        logger.debug("Model already initialized, returning cached instance")
        return _model, _tokenizer, _device
    
    try:
        logger.info(f"Initializing summarization model: {model_name}")
        
        # Determine device
        _device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        logger.info(f"Using device: {_device}")
        
        # Load tokenizer
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load model with optimal precision
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        _model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=dtype
        )
        
        # Move to device
        _model = _model.to(_device)
        
        # Set evaluation mode
        _model.eval()
        
        logger.info(f"Model initialized successfully on {_device}")
        
        return _model, _tokenizer, _device
    
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")
        raise SummarizationError(f"Model initialization failed: {str(e)}")


def _clean_text(text: str) -> str:
    """
    Clean and normalize input text.
    
    Removes extra whitespace, special characters while preserving readability.
    
    Args:
        text: Raw text to clean.
    
    Returns:
        Cleaned text.
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove control characters but keep punctuation
    text = re.sub(r'[\x00-\x1f\x7f]', '', text)
    
    return text


def _split_into_chunks(
    text: str,
    max_chunk_length: int = 512
) -> List[str]:
    """
    Split long text into manageable chunks for summarization.
    
    Ensures chunks respect sentence boundaries to maintain semantic coherence.
    BART tokenizer has ~1024 token limit, so 512 character chunks are safe.
    
    Args:
        text: Input text to split.
        max_chunk_length: Maximum length of each chunk in characters.
    
    Returns:
        List of text chunks.
    """
    # Split into sentences using common sentence delimiters
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return [text] if text.strip() else []
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence) + 1  # +1 for space
        
        # If single sentence exceeds max, still include it
        if sentence_length > max_chunk_length and not current_chunk:
            chunks.append(sentence)
            continued = True
        else:
            # Check if adding this sentence exceeds limit
            if current_length + sentence_length > max_chunk_length and current_chunk:
                # Save current chunk and start new one
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                # Add to current chunk
                current_chunk.append(sentence)
                current_length += sentence_length
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    logger.debug(f"Text split into {len(chunks)} chunks")
    return chunks


def _summarize_single_chunk(
    text: str,
    max_length: int = 120,
    min_length: int = 30
) -> str:
    """
    Generate summary for a single text chunk.
    
    Uses deterministic beam search (no sampling) for consistent output.
    
    Args:
        text: Input text chunk.
        max_length: Maximum tokens in summary.
        min_length: Minimum tokens in summary.
    
    Returns:
        Generated summary.
    
    Raises:
        SummarizationError: If summarization fails.
    """
    model, tokenizer, device = _initialize_model()
    
    try:
        # Tokenize input
        inputs = tokenizer(
            text,
            max_length=512,
            truncation=True,
            return_tensors="pt"
        ).to(device)
        
        # Generate summary with deterministic settings
        with torch.no_grad():
            summary_ids = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=max_length,
                min_length=min_length,
                num_beams=4,                    # Beam search (deterministic)
                do_sample=False,                # No sampling for reproducibility
                early_stopping=True,
                length_penalty=2.0,             # Encourage longer summaries
            )
        
        # Decode summary
        summary = tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )
        
        return summary.strip()
    
    except Exception as e:
        logger.error(f"Chunk summarization failed: {str(e)}")
        raise SummarizationError(f"Failed to summarize chunk: {str(e)}")


def _merge_summaries(summaries: List[str]) -> str:
    """
    Merge summaries from multiple chunks into a final summary.
    
    If only one summary exists, returns it as-is.
    If multiple summaries exist, recursively summarizes them together.
    
    Args:
        summaries: List of chunk summaries.
    
    Returns:
        Final merged summary.
    
    Raises:
        SummarizationError: If merging fails.
    """
    if not summaries:
        raise SummarizationError("No summaries to merge")
    
    if len(summaries) == 1:
        return summaries[0]
    
    logger.debug(f"Merging {len(summaries)} summaries")
    
    # Combine all summaries
    combined = " ".join(summaries)
    
    # If combined summary is short enough, just return it
    if len(combined) <= 512:
        return combined
    
    # Otherwise, summarize the combined summaries recursively
    try:
        merged = _summarize_single_chunk(
            combined,
            max_length=150,
            min_length=30
        )
        return merged
    except SummarizationError as e:
        logger.error(f"Failed to merge summaries: {str(e)}")
        return " ".join(summaries[:2])  # Fallback: return first 2 summaries


def generate_summary(
    text: str,
    max_length: int = 120,
    min_length: int = 30
) -> str:
    """
    Generate a concise summary for input text.
    
    Handles long documents by chunking, summarizing each chunk,
    and then merging the summaries. Uses deterministic beam search
    for consistent, reproducible output.
    
    Key Features:
    - Efficient single-load model initialization (cached in global scope)
    - Automatic chunking for texts longer than 512 characters
    - Sentence-boundary-aware splitting for semantic coherence
    - Deterministic output using beam search without sampling
    - Configurable summary length parameters
    
    Args:
        text: Input text to summarize (required, non-empty).
        max_length: Maximum length of summary in tokens. Default: 120.
        min_length: Minimum length of summary in tokens. Default: 30.
    
    Returns:
        str: The generated summary.
    
    Raises:
        ValueError: If input text is empty or invalid.
        SummarizationError: If model loading or inference fails.
    
    Example:
        >>> text = "Long document text here..."
        >>> summary = generate_summary(text)
        >>> print(summary)
        "Concise summary of the document."
    """
    # Validate input
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string")
    
    text = text.strip()
    if len(text) < 20:
        raise ValueError("Input text must be at least 20 characters long")
    
    try:
        logger.info(f"Starting summarization. Input length: {len(text)} characters")
        
        # Clean text
        cleaned_text = _clean_text(text)
        logger.debug(f"Cleaned text length: {len(cleaned_text)} characters")
        
        # Split into chunks if necessary
        chunks = _split_into_chunks(cleaned_text, max_chunk_length=512)
        
        # Summarize each chunk
        logger.debug(f"Summarizing {len(chunks)} chunk(s)")
        summaries = []
        
        for i, chunk in enumerate(chunks, 1):
            try:
                chunk_summary = _summarize_single_chunk(
                    chunk,
                    max_length=max_length,
                    min_length=min_length
                )
                summaries.append(chunk_summary)
                logger.debug(f"Summarized chunk {i}/{len(chunks)}")
            except SummarizationError as e:
                logger.warning(f"Failed to summarize chunk {i}: {str(e)}")
                summaries.append(chunk[:200])  # Fallback: use text excerpt
        
        # Merge summaries from all chunks
        final_summary = _merge_summaries(summaries)
        
        logger.info(
            f"Summarization complete. "
            f"Input: {len(text)} chars, Output: {len(final_summary)} chars, "
            f"Compression ratio: {(1 - len(final_summary)/len(text))*100:.1f}%"
        )
        
        return final_summary
    
    except ValueError:
        raise
    except SummarizationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during summarization: {str(e)}")
        raise SummarizationError(f"Summarization failed: {str(e)}")
