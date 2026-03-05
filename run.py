"""
Entry point for running the application from command line.

Supports running the Streamlit app or tests.
"""

import sys
import subprocess
from pathlib import Path


def run_streamlit():
    """Run the Streamlit application."""
    app_path = Path(__file__).parent / "app" / "main.py"
    subprocess.run(["streamlit", "run", str(app_path)])


def run_tests(args=None):
    """Run pytest tests."""
    cmd = ["pytest", "tests/", "-v"]
    if args:
        cmd.extend(args)
    subprocess.run(cmd)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python run.py [command]")
        print("\nAvailable commands:")
        print("  streamlit - Run the Streamlit web application")
        print("  test      - Run the test suite")
        print("\nExample:")
        print("  python run.py streamlit")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "streamlit":
        run_streamlit()
    elif command == "test":
        run_tests(sys.argv[2:] if len(sys.argv) > 2 else None)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
