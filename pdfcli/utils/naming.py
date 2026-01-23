"""Utilities for file naming."""

import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """
    Create a safe filename from a string.
    
    Removes or replaces characters that are not safe for filenames.
    
    Args:
        name: Original name.
    
    Returns:
        Sanitized filename.
    """
    # Remove or replace unsafe characters
    safe = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove leading/trailing whitespace and dots
    safe = safe.strip().strip('.')
    # Replace multiple underscores/spaces with single underscore
    safe = re.sub(r'[_\s]+', '_', safe)
    
    return safe or "unnamed"


def generate_output_name(
    stem: str,
    suffix: str = "",
    extension: str = ".pdf"
) -> str:
    """
    Generate output filename with optional suffix.
    
    Args:
        stem: Base name without extension.
        suffix: Optional suffix to add (e.g., "_compressed").
        extension: File extension with dot.
    
    Returns:
        Complete filename.
    """
    safe_stem = sanitize_filename(stem)
    return f"{safe_stem}{suffix}{extension}"


def format_page_number(page_num: int, total_pages: int) -> str:
    """
    Format page number with leading zeros.
    
    Args:
        page_num: Current page number (1-indexed).
        total_pages: Total number of pages.
    
    Returns:
        Formatted page number string.
    """
    # Calculate required width based on total pages
    width = len(str(total_pages))
    # Minimum width of 3 for aesthetics
    width = max(width, 3)
    
    return str(page_num).zfill(width)
