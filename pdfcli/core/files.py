"""File operations: search, filter, natural sort."""

import re
from pathlib import Path
from typing import Callable

from pdfcli.core.config import INPUT_DIR, IMAGE_EXTENSIONS, PDF_EXTENSION


def natural_sort_key(path: Path) -> list:
    """
    Generate a key for natural sorting.
    Splits filename into text and numeric parts for proper ordering.
    Example: file1, file2, file10 (not file1, file10, file2)
    """
    text = path.stem.lower()
    parts = re.split(r'(\d+)', text)
    return [int(part) if part.isdigit() else part for part in parts]


def _list_files(
    directory: Path | None,
    filter_fn: Callable[[Path], bool],
) -> list[Path]:
    """
    List files in directory matching filter, naturally sorted.
    
    Args:
        directory: Directory to search. Defaults to INPUT_DIR.
        filter_fn: Function to filter files.
    
    Returns:
        List of matching file paths, naturally sorted.
    """
    directory = directory or INPUT_DIR
    
    if not directory.exists():
        return []
    
    files = [f for f in directory.iterdir() if f.is_file() and filter_fn(f)]
    return sorted(files, key=natural_sort_key)


def list_images(directory: Path | None = None) -> list[Path]:
    """
    List all supported image files in directory, naturally sorted.
    
    Args:
        directory: Directory to search. Defaults to INPUT_DIR.
    
    Returns:
        List of image file paths, naturally sorted.
    """
    return _list_files(
        directory,
        lambda f: f.suffix.lower() in IMAGE_EXTENSIONS,
    )


def list_pdfs(directory: Path | None = None) -> list[Path]:
    """
    List all PDF files in directory, naturally sorted.
    
    Args:
        directory: Directory to search. Defaults to INPUT_DIR.
    
    Returns:
        List of PDF file paths, naturally sorted.
    """
    return _list_files(
        directory,
        lambda f: f.suffix.lower() == PDF_EXTENSION,
    )


def count_files_summary() -> dict[str, int]:
    """
    Count images and PDFs in INPUT_DIR.
    
    Returns:
        Dictionary with 'images' and 'pdfs' counts.
    """
    return {
        "images": len(list_images()),
        "pdfs": len(list_pdfs()),
    }
