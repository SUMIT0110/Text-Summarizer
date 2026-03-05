"""
Streamlit Web Application for Text Summarization.

Interactive web interface for the text summarization system using BART transformer.
Deprecated: Use app/app.py instead for the new UI.
"""

import streamlit as st
import time

from models.summarizer import generate_summary, SummarizationError
from utils.text_processor import TextProcessor
from utils.logger import logger


# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea, .stTextInput {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.title("📝 AI Text Summarizer")
    st.markdown("*Powered by BART Transformer Model - facebook/bart-large-cnn*")
    st.divider()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.info("""
        **Model:** facebook/bart-large-cnn
        
        **Features:**
        - Deterministic summarization (no sampling)
        - Automatic chunk processing for long texts
        - Sentence-boundary-aware splitting
        """)
        
        st.header("Summary Parameters")
        max_length = st.slider(
            "Maximum Summary Length (tokens)",
            min_value=30,
            max_value=200,
            value=120,
            step=10,
            help="Maximum number of tokens in the summary"
        )
        
        min_length = st.slider(
            "Minimum Summary Length (tokens)",
            min_value=10,
            max_value=100,
            value=30,
            step=5,
            help="Minimum number of tokens in the summary"
        )
    
    # Main content
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.header("📄 Input Text")
        input_text = st.text_area(
            label="Paste your text here",
            placeholder="Enter the text you want to summarize...",
            height=350,
            label_visibility="collapsed"
        )
    
    with col2:
        st.header("✨ Summary")
        summary_placeholder = st.empty()
    
    # Process button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        summarize_button = st.button(
            "🚀 Summarize",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        clear_button = st.button(
            "🔄 Clear",
            use_container_width=True
        )
    
    # Handle button clicks
    if clear_button:
        st.rerun()
    
    if summarize_button:
        if not input_text.strip():
            st.error("❌ Please enter some text to summarize")
            return
        
        # Validate text
        is_valid, message = TextProcessor.validate_text(
            input_text,
            min_length=20,
            max_length=5000
        )
        if not is_valid:
            st.error(f"❌ {message}")
            return
        
        # Generate summary
        try:
            with st.spinner("🤔 Generating summary..."):
                start_time = time.time()
                
                # Get text stats before
                stats = TextProcessor.get_text_stats(input_text)
                
                # Generate summary using the deterministic engine
                summary = generate_summary(
                    input_text,
                    max_length=max_length,
                    min_length=min_length
                )
                
                elapsed_time = time.time() - start_time
                
                # Display summary
                with col2:
                    summary_placeholder.text_area(
                        label="Generated Summary",
                        value=summary,
                        height=350,
                        disabled=True,
                        label_visibility="collapsed"
                    )
            
            # Display statistics
            st.divider()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Input Words",
                    stats["word_count"]
                )
            
            with col2:
                summary_stats = TextProcessor.get_text_stats(summary)
                compression_ratio = (
                    (stats["word_count"] - summary_stats["word_count"]) 
                    / stats["word_count"] * 100
                ) if stats["word_count"] > 0 else 0
                st.metric(
                    "Summary Words",
                    summary_stats["word_count"],
                    delta=f"-{compression_ratio:.1f}%"
                )
            
            with col3:
                st.metric(
                    "Compression Ratio",
                    f"{compression_ratio:.1f}%"
                )
            
            with col4:
                st.metric(
                    "Processing Time",
                    f"{elapsed_time:.2f}s"
                )
            
            logger.info(f"Summary generated successfully. Time: {elapsed_time:.2f}s")
            st.success("✅ Summary generated successfully!")
        
        except SummarizationError as e:
            logger.error(f"Summarization error: {str(e)}")
            st.error(f"❌ Summarization Error: {str(e)}")
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            st.error(f"❌ Input Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            st.error(f"❌ Error: {str(e)}")
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    **AI Text Summarizer v2.0** | Powered by BART & PyTorch
    
    **How it works:**
    1. 📥 Input long-form text (articles, documents, etc.)
    2. 🔄 System automatically chunks long text for optimal processing
    3. 🧠 BART model generates summaries for each chunk
    4. 🔗 Summaries are merged into a final concise output
    5. 📊 View compression statistics and processing time
    
    **Key Features:**
    - ✅ Deterministic output (reproducible results)
    - ✅ Automatic chunk handling for long documents
    - ✅ GPU acceleration (CUDA) with CPU fallback
    - ✅ Configurable summary length parameters
    """)


if __name__ == "__main__":
    main()
