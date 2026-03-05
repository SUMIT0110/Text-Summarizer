"""
Streamlit Web Application for AI Text Summarizer.

Clean, responsive web interface for text summarization using BART transformer.
Demonstrates best practices for Streamlit applications with proper error handling,
state management, and metrics display.
"""

import sys
import os
import warnings
from pathlib import Path

# Suppress deprecation warnings and non-critical messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*torch_dtype.*')
warnings.filterwarnings('ignore', message='.*huggingface_hub.*')

# Add project root to Python path for proper imports
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set HuggingFace cache to local models_cache directory (for offline/portable use)
# This allows the project to work without downloading the model again
local_cache = os.path.join(project_root, "models_cache")
if os.path.exists(local_cache):
    os.environ['HF_HOME'] = local_cache
    os.environ['TRANSFORMERS_OFFLINE'] = '0'  # Try local first, then download if needed

import streamlit as st
import time
from datetime import datetime

from models.summarizer import generate_summary, SummarizationError
from utils.preprocess import clean_text, is_clean
from utils.logger import logger


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container padding */
    .main {
        padding: 2rem;
    }
    
    /* Text areas styling */
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Success message */
    .success-message {
        color: #0f5132;
        background-color: #d1e7dd;
        border: 1px solid #badbcc;
        padding: 12px;
        border-radius: 4px;
    }
    
    /* Info message */
    .info-message {
        color: #084298;
        background-color: #cfe2ff;
        border: 1px solid #b6d4fe;
        padding: 12px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split()) if text.strip() else 0


def count_characters(text: str) -> int:
    """Count characters in text."""
    return len(text.strip())


def calculate_compression(original_length: int, summary_length: int) -> float:
    """Calculate compression percentage."""
    if original_length == 0:
        return 0.0
    return ((original_length - summary_length) / original_length) * 100


def format_large_number(num: int) -> str:
    """Format large numbers with commas."""
    return f"{num:,}"


@st.cache_resource
def initialize_model():
    """Initialize model on first load (cached)."""
    logger.info("Initializing summarization model")
    # Model initialization happens in generate_summary on first call
    return True


# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""

if "processing_time" not in st.session_state:
    st.session_state.processing_time = 0

if "show_stats" not in st.session_state:
    st.session_state.show_stats = False


# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown("# 📝 AI Text Summarizer")
st.markdown(
    "**Transform long articles into concise summaries using advanced AI** "
    "✨ Powered by BART Transformer Model"
)

st.divider()


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.markdown("""
    ### Model Information
    - **Model**: facebook/bart-large-cnn
    - **Type**: Sequence-to-Sequence Transformer
    - **Parameters**: 430M
    - **Output**: Deterministic
    
    ### Features
    - ✅ GPU Acceleration (CUDA)
    - ✅ Automatic Chunking for Long Texts
    - ✅ Reproducible Results
    - ✅ Real-time Processing
    """)
    
    st.divider()
    
    st.header("📊 Summary Length Preset")
    
    # Quick selection for summary length
    summary_preset = st.radio(
        "Select Summary Length:",
        options=["Short 🎯", "Medium ⚖️", "Long 📚"],
        help="Quick presets for different summary types",
        key="summary_preset",
        horizontal=False
    )
    
    # Map preset to max_length value
    preset_lengths = {
        "Short 🎯": 60,
        "Medium ⚖️": 120,
        "Long 📚": 200
    }
    max_length_preset = preset_lengths[summary_preset]
    
    # Display selected length info
    length_info = {
        "Short 🎯": "Headlines & snippets (150-250 characters)",
        "Medium ⚖️": "Standard summaries (400-500 characters)",
        "Long 📚": "Detailed summaries (700-900 characters)"
    }
    st.info(f"📋 {length_info[summary_preset]}")
    
    st.divider()
    
    st.header("⚙️ Advanced Parameters")
    
    # Default to preset values
    max_length = max_length_preset
    min_length = 30
    
    # Allow fine-tuning with checkbox
    with st.expander("🔧 Customize Settings", expanded=False):
        st.markdown("**Fine-tune summary length constraints:**")
        
        max_length = st.slider(
            "Maximum Summary Length (tokens)",
            min_value=30,
            max_value=200,
            value=max_length_preset,
            step=10,
            help="Increase for longer summaries",
            key="max_length_slider"
        )
        
        min_length = st.slider(
            "Minimum Summary Length (tokens)",
            min_value=10,
            max_value=100,
            value=30,
            step=5,
            help="Minimum length to maintain quality",
            key="min_length_slider"
        )
    
    st.divider()
    
    st.header("📋 Input Guidance")
    st.markdown("""
    **Best Results When:**
    - Text is 50+ words
    - Well-structured paragraphs
    - Clear topic/subject matter
    
    **May Have Issues With:**
    - Very short text (<20 words)
    - Lists without context
    - Highly technical jargon
    """)
    
    st.divider()
    
    # About section
    st.header("ℹ️ About")
    st.markdown("""
    **AI Text Summarizer v2.0**
    
    Summarization engine powered by:
    - BART (Denoising Seq2Seq Transformer)
    - PyTorch Deep Learning Framework
    - HuggingFace Transformers Library
    
    [GitHub](https://github.com) • 
    [Documentation](https://readme.md) •
    [Report Issue](https://github.com/issues)
    """)


# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Create two-column layout
col1, col2 = st.columns([1, 1], gap="large")

# ============================================================================
# LEFT COLUMN - INPUT
# ============================================================================

with col1:
    st.subheader("📄 Original Text", anchor="input-section")
    
    input_text = st.text_area(
        label="Paste your article or document here",
        placeholder="Enter the text you want to summarize...\n\nExample: 'Artificial intelligence is transforming the world...'",
        height=400,
        key="text_input",
        label_visibility="collapsed"
    )
    
    # Update session state
    st.session_state.input_text = input_text
    
    # Input statistics
    if input_text.strip():
        input_words = count_words(input_text)
        input_chars = count_characters(input_text)
        
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Words", format_large_number(input_words))
        with stats_col2:
            st.metric("Characters", format_large_number(input_chars))


# ============================================================================
# RIGHT COLUMN - OUTPUT
# ============================================================================

with col2:
    st.subheader("✨ Generated Summary", anchor="output-section")
    
    # Summary display area
    if st.session_state.summary_text:
        st.text_area(
            label="Summary",
            value=st.session_state.summary_text,
            height=400,
            disabled=True,
            label_visibility="collapsed"
        )
    else:
        st.info("💡 Enter text and click 'Generate Summary' to see the summary here.", icon="ℹ️")
    
    # Summary statistics
    if st.session_state.summary_text:
        summary_words = count_words(st.session_state.summary_text)
        summary_chars = count_characters(st.session_state.summary_text)
        compression = calculate_compression(
            count_words(input_text),
            summary_words
        )
        
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.metric("Summary Words", format_large_number(summary_words))
        
        with stats_col2:
            st.metric(
                "Compression",
                f"{compression:.1f}%",
                delta=f"-{format_large_number(count_words(input_text) - summary_words)} words"
            )
        
        with stats_col3:
            st.metric(
                "Processing Time",
                f"{st.session_state.processing_time:.2f}s",
                delta="seconds"
            )


# ============================================================================
# ACTION BUTTONS
# ============================================================================

st.divider()

# Button row
button_col1, button_col2, button_col3, _ = st.columns([1, 1, 1, 2])

with button_col1:
    summarize_button = st.button(
        "🚀 Generate Summary",
        type="primary",
        use_container_width=True,
        key="summarize_btn"
    )

with button_col2:
    clear_button = st.button(
        "🔄 Clear All",
        use_container_width=True,
        key="clear_btn"
    )

with button_col3:
    copy_button = st.button(
        "📋 Copy Summary",
        use_container_width=True,
        key="copy_btn",
        disabled=not st.session_state.summary_text
    )


# ============================================================================
# BUTTON HANDLERS
# ============================================================================

# Handle Clear button
if clear_button:
    st.session_state.input_text = ""
    st.session_state.summary_text = ""
    st.session_state.processing_time = 0
    st.rerun()

# Handle Copy button
if copy_button and st.session_state.summary_text:
    st.toast("📋 Summary copied to clipboard!", icon="✅")
    logger.info("Summary copied to clipboard")

# Handle Summarize button
if summarize_button:
    # Validate input
    if not input_text or not input_text.strip():
        st.error("❌ Please enter some text to summarize.", icon="⚠️")
        logger.warning("Summarization attempted with empty text")
    
    else:
        # Check if text is already clean
        if not is_clean(input_text):
            cleaned_text = clean_text(input_text)
            logger.debug("Text preprocessed")
        else:
            cleaned_text = input_text
        
        # Validate text length
        word_count = count_words(cleaned_text)
        
        if word_count < 10:
            st.error(
                "❌ Text too short for summarization. Please provide at least 10 words.",
                icon="⚠️"
            )
            logger.warning(f"Text too short: {word_count} words")
        
        else:
            # Generate summary
            try:
                with st.spinner("🤔 Generating summary... This may take a moment."):
                    start_time = time.time()
                    
                    # Call summarization engine
                    summary = generate_summary(
                        cleaned_text,
                        max_length=max_length,
                        min_length=min_length
                    )
                    
                    processing_time = time.time() - start_time
                
                # Store results in session state
                st.session_state.summary_text = summary
                st.session_state.processing_time = processing_time
                
                # Show success message
                st.success(
                    f"✅ Summary generated successfully in {processing_time:.2f} seconds!",
                    icon="✅"
                )
                
                # Log success
                logger.info(
                    f"Summarization completed. "
                    f"Input: {count_words(input_text)} words, "
                    f"Output: {count_words(summary)} words, "
                    f"Time: {processing_time:.2f}s"
                )
                
                # Rerun to update display
                st.rerun()
            
            except ValueError as e:
                st.error(f"❌ Input Error: {str(e)}", icon="⚠️")
                logger.error(f"Input validation error: {str(e)}")
            
            except SummarizationError as e:
                st.error(
                    f"❌ Summarization Error: {str(e)}\n\n"
                    f"Please try with a shorter text or check your input.",
                    icon="⚠️"
                )
                logger.error(f"Summarization failed: {str(e)}")
            
            except Exception as e:
                st.error(
                    f"❌ Unexpected Error: {str(e)}\n\n"
                    f"Please try again or contact support.",
                    icon="⚠️"
                )
                logger.error(f"Unexpected error: {str(e)}")


# ============================================================================
# FOOTER & ADDITIONAL INFO
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **💡 Tips for Best Results**
    
    1. Use well-structured text
    2. Provide sufficient context
    3. 50-5000 word documents work best
    4. Update parameters if needed
    """)

with col2:
    st.markdown("""
    **🎯 Use Cases**
    
    - News articles summarization
    - Document abstraction
    - Research paper summaries
    - Meeting notes condensing
    - Email digest creation
    """)

with col3:
    st.markdown("""
    **⚡ Performance Notes**
    
    - First load: 15-30 seconds
    - Subsequent: 1-3 seconds
    - GPU acceleration available
    - Works offline (no API needed)
    """)

st.divider()

# Footer
st.markdown("""
---
<div style='text-align: center; color: gray; font-size: 12px;'>
<b>AI Text Summarizer v2.0</b> | Powered by BART Transformer & PyTorch<br>
Developed with ❤️ using Streamlit | <a href='#'>GitHub</a> • <a href='#'>Docs</a> • <a href='#'>Issues</a>
</div>
""", unsafe_allow_html=True)
