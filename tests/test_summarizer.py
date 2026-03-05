"""
Unit tests for the Text Summarization Module
Tests the core summarizer functionality using Python's unittest framework

Run tests with:
    python -m unittest tests.test_summarizer
    python -m unittest tests.test_summarizer -v
    python -m unittest discover -s tests -p "test_*.py"
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.summarizer import generate_summary


class TestSummarizerShortText(unittest.TestCase):
    """Test summarizing short text"""

    def test_summarize_short_text(self):
        """Test: Summarizing short text"""
        short_text = (
            "Machine learning is a subset of artificial intelligence. "
            "It allows computers to learn from data without being explicitly programmed. "
            "Deep learning uses neural networks with multiple layers."
        )

        try:
            result = generate_summary(short_text)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            print(f"\n✓ Short text summary generated: {result[:80]}...")
        except ValueError as e:
            # Short texts may raise ValueError - this is acceptable
            self.assertIn("short", str(e).lower())
            print(f"\n✓ Short text correctly handled: {e}")

    def test_short_text_is_string(self):
        """Test that short text output is valid string"""
        text = (
            "Python is a programming language. "
            "It is used for web development, data science, and AI. "
            "The language is easy to learn."
        )

        try:
            result = generate_summary(text)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            self.assertTrue(result.strip())
        except ValueError:
            pass


class TestSummarizerLongText(unittest.TestCase):
    """Test summarizing long text"""

    def test_summarize_long_text(self):
        """Test: Summarizing long text"""
        long_text = """
        Artificial intelligence is rapidly transforming industries worldwide. From healthcare 
        to finance, from manufacturing to retail, AI applications are delivering significant value. 
        Research institutions are racing to develop more capable models while companies are investing 
        heavily in AI infrastructure and talent. Machine learning engineers are in high demand as 
        organizations seek to leverage AI for competitive advantage.

        Deep learning, a subset of machine learning, uses neural networks with multiple layers. 
        These neural networks can process vast amounts of data and discover patterns that humans 
        might miss. Convolutional neural networks excel at image recognition tasks. Recurrent neural 
        networks work well with sequential data like time series or natural language.

        Natural language processing allows computers to understand and generate human language. 
        This technology powers virtual assistants, translation services, and chatbots. Large language 
        models like GPT have demonstrated remarkable capabilities in understanding context and 
        generating coherent text.

        However, concerns about AI safety, bias, and ethics continue to grow among researchers and 
        policymakers. The future of artificial intelligence depends on balancing innovation with 
        responsible development practices. Training data quality is crucial for building fair and 
        accurate AI systems. Many organizations are establishing AI ethics committees to guide their 
        development practices.
        """

        result = generate_summary(long_text, max_length=120, min_length=30)

        # Assertions
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

        # Long text summary should be meaningful
        word_count = len(result.split())
        self.assertGreater(word_count, 5)

        print(f"\n✓ Long text summary ({word_count} words):")
        print(f"  {result}")

    def test_long_text_compression(self):
        """Test that long text summary is compressed"""
        long_text = "This is a test sentence. " * 50

        result = generate_summary(long_text, max_length=100, min_length=20)

        original_length = len(long_text.split())
        summary_length = len(result.split())

        self.assertLess(summary_length, original_length)
        print(
            f"\n✓ Compression: {original_length} words → "
            f"{summary_length} words"
        )

    def test_long_text_parameter_effect(self):
        """Test that max_length parameter affects output for long text"""
        long_text = """
        Technology is advancing rapidly. Cloud computing has transformed how organizations 
        manage their infrastructure. Serverless computing reduces operational overhead. Container 
        orchestration with Kubernetes enables efficient resource utilization. DevOps practices 
        have improved software delivery cycles. Machine learning operations (MLOps) is emerging 
        as a critical discipline. Continuous integration and continuous deployment (CI/CD) are 
        now industry standards.
        """

        summary_short = generate_summary(long_text, max_length=50, min_length=10)
        summary_long = generate_summary(long_text, max_length=150, min_length=30)

        short_words = len(summary_short.split())
        long_words = len(summary_long.split())

        # Longer max_length should generally produce longer summary
        self.assertGreater(long_words, short_words)
        
        print(
            f"\n✓ Parameter effect verified: "
            f"max=50 → {short_words} words, max=150 → {long_words} words"
        )


class TestSummarizerEmptyInput(unittest.TestCase):
    """Test handling empty input"""

    def test_handle_empty_input(self):
        """Test: Handling empty input"""
        with self.assertRaises(ValueError):
            generate_summary("")

        print("\n✓ Empty input correctly raises ValueError")

    def test_handle_whitespace_only(self):
        """Test handling whitespace-only input"""
        with self.assertRaises(ValueError):
            generate_summary("   \n\n\t  ")

        print("\n✓ Whitespace-only input correctly raises ValueError")

    def test_handle_none_input(self):
        """Test handling None input"""
        with self.assertRaises((TypeError, AttributeError, ValueError)):
            generate_summary(None)

        print("\n✓ None input correctly handled")

    def test_handle_very_short_input(self):
        """Test handling very short input"""
        with self.assertRaises(ValueError):
            generate_summary("Hello")

        print("\n✓ Very short input correctly raises ValueError")


class TestSummarizerOutputShorterThanInput(unittest.TestCase):
    """Test verifying output is shorter than input"""

    def test_output_shorter_than_input(self):
        """Test: Verifying output is shorter than input"""
        text = """
        The Internet of Things has emerged as a transformative technology ecosystem. 
        Connected devices are proliferating across industries and consumer markets. Smart homes 
        incorporate IoT sensors for climate control, security, and energy management. Industrial 
        IoT applications improve manufacturing efficiency and predictive maintenance. Healthcare 
        providers use IoT devices for remote monitoring and patient care. IoT platforms collect 
        and analyze massive amounts of data from distributed devices.

        Edge computing processes IoT data closer to the source, reducing latency. 5G networks 
        enable high-speed, low-latency IoT communications. Security remains a critical concern 
        as IoT devices are often vulnerable to attacks. Standardization efforts are underway to 
        ensure interoperability across different IoT platforms.
        """

        result = generate_summary(text)

        original_words = len(text.split())
        summary_words = len(result.split())

        self.assertLess(summary_words, original_words)

        compression_percentage = (1 - summary_words / original_words) * 100
        self.assertGreater(compression_percentage, 50)

        print(f"\n✓ Output shorter than input verified:")
        print(f"  Original: {original_words} words")
        print(f"  Summary: {summary_words} words")
        print(f"  Compression: {compression_percentage:.1f}%")

    def test_multiple_texts_compression(self):
        """Test compression across multiple different texts"""
        texts = [
            "Blockchain technology enables decentralized systems. " * 20,
            "Cybersecurity threats continue to evolve. " * 20,
            "Climate change impacts global economies. " * 20,
        ]

        for i, text in enumerate(texts):
            result = generate_summary(text)
            original_words = len(text.split())
            summary_words = len(result.split())

            self.assertLess(summary_words, original_words)

            compression = (1 - summary_words / original_words) * 100
            self.assertGreater(compression, 30)

        print(f"\n✓ All {len(texts)} texts compressed successfully")

    def test_compression_ratio_reasonable(self):
        """Test that compression ratio is reasonable"""
        text = """
        Renewable energy sources are becoming increasingly important. Solar power generation has 
        become more cost-effective. Wind turbines harness kinetic energy from wind. Hydroelectric 
        power provides consistent energy output. Geothermal energy taps into Earth's internal heat. 
        Biomass can be converted to energy. These renewable sources reduce dependence on fossil 
        fuels. Battery storage technology enables energy management. Grid modernization supports 
        renewable energy integration. The transition to renewable energy is accelerating globally.
        """

        result = generate_summary(text, max_length=120, min_length=30)

        original_words = len(text.split())
        summary_words = len(result.split())
        compression = (1 - summary_words / original_words) * 100

        # Compression should be between 30% and 90%
        self.assertGreater(compression, 30)
        self.assertLess(compression, 90)

        print(f"\n✓ Compression ratio is reasonable: {compression:.1f}%")


class TestSummarizerDeterministic(unittest.TestCase):
    """Test that output is deterministic"""

    def test_deterministic_output(self):
        """Test that same input produces same output"""
        text = """
        Quantum computing represents a revolutionary approach to computation. Quantum bits or qubits 
        can exist in superposition. This allows quantum computers to process multiple possibilities 
        simultaneously. Quantum entanglement enables correlation between qubits. Error correction is 
        a significant challenge in quantum computing. Quantum algorithms like Shor's algorithm offer 
        exponential speedups for certain problems.
        """

        result1 = generate_summary(text, max_length=80, min_length=20)
        result2 = generate_summary(text, max_length=80, min_length=20)

        self.assertEqual(result1, result2)

        print("\n✓ Output is deterministic (identical for same input)")


class TestSummarizerErrorHandling(unittest.TestCase):
    """Test error handling for various edge cases"""

    def test_invalid_max_length(self):
        """Test with invalid max_length parameter"""
        text = "This is a sample text for testing. " * 10

        with self.assertRaises(ValueError):
            generate_summary(text, max_length=0)

        print("\n✓ Invalid max_length correctly rejected")

    def test_max_less_than_min_length(self):
        """Test when max_length is less than min_length"""
        text = "This is a sample text for testing. " * 10

        with self.assertRaises(ValueError):
            generate_summary(text, max_length=20, min_length=50)

        print("\n✓ Invalid length parameters correctly rejected")

    def test_special_characters(self):
        """Test handling text with special characters"""
        text = """
        The company's Q3 revenue was $1.5M (30% YoY growth)!
        They operate in 5 countries: USA, UK, Canada, Australia & Germany.
        Email: contact@example.com | Website: https://example.com
        Key metrics: 95.5% uptime, <50ms latency, 99.9% accuracy rate.
        """

        result = generate_summary(text)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

        print(f"\n✓ Special characters handled correctly")


if __name__ == "__main__":
    unittest.main(verbosity=2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
