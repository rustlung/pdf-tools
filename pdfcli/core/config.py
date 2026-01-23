"""Configuration and paths for PDF Tools."""

from pathlib import Path

# Root directory (where main.py is located)
ROOT = Path(__file__).resolve().parent.parent.parent

# Input/Output directories
INPUT_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output"

# Supported image extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}

# Supported PDF extension
PDF_EXTENSION = ".pdf"


def ensure_dirs() -> None:
    """Create input and output directories if they don't exist."""
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
