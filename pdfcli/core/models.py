"""Data models for PDF Tools operations."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class ImagesToPdfOptions:
    """Options for images to PDF conversion."""
    output_name: str = "combined"
    image_paths: list[Path] | None = None  # If None, use all images from INPUT_DIR


@dataclass
class PdfToImagesOptions:
    """Options for PDF to images extraction."""
    source_pdf: Path
    dpi: int = 150
    output_format: Literal["png", "jpg"] = "png"


@dataclass
class CompressPdfOptions:
    """Options for PDF compression."""
    source_pdf: Path
    preset: Literal["screen", "ebook", "printer", "prepress"] = "ebook"


@dataclass
class OperationResult:
    """Result of an operation."""
    success: bool
    message: str
    output_path: Path | None = None
    files_count: int = 0
