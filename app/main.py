import sys
from pathlib import Path

# Make the repo root importable so `app` and `src` both resolve
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ui import render  # noqa: E402


def main() -> None:
    """Entry point script for launching the application."""
    render()


# Streamlit executes this file as a script (not as "__main__"),
# so call main() directly instead of using an `if __name__ == "__main__":` guard.
main()