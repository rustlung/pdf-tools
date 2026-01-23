"""Operation: Compress PDF using Ghostscript."""

from pathlib import Path
from typing import Literal

from pdfcli.core.config import OUTPUT_DIR
from pdfcli.core.errors import OperationError
from pdfcli.core.models import CompressPdfOptions, OperationResult
from pdfcli.services.ghostscript import run_ghostscript
from pdfcli.utils.naming import sanitize_filename


def compress_pdf(options: CompressPdfOptions) -> OperationResult:
    """
    Compress a PDF file using Ghostscript.
    
    Output file is named: <original_stem>_compressed_<preset>.pdf
    
    Args:
        options: Operation options including source PDF and preset.
    
    Returns:
        OperationResult with success status and output path.
    
    Raises:
        OperationError: If compression fails.
        ToolNotFoundError: If Ghostscript is not available.
    """
    source_pdf = options.source_pdf
    preset = options.preset
    
    # Validate source
    if not source_pdf.exists():
        raise OperationError(f"Файл не найден: {source_pdf}")
    
    # Get original file size for comparison
    original_size = source_pdf.stat().st_size
    
    # Generate output filename
    safe_stem = sanitize_filename(source_pdf.stem)
    output_name = f"{safe_stem}_compressed_{preset}.pdf"
    output_path = OUTPUT_DIR / output_name
    
    # Run Ghostscript (raises ToolNotFoundError or OperationError on failure)
    run_ghostscript(source_pdf, output_path, preset)
    
    # Check if output was created
    if not output_path.exists():
        raise OperationError(
            "Ghostscript не создал выходной файл.\n"
            "Возможно, входной PDF повреждён или защищён."
        )
    
    # Calculate compression stats
    new_size = output_path.stat().st_size
    reduction = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0
    
    # Format sizes for display
    original_mb = original_size / (1024 * 1024)
    new_mb = new_size / (1024 * 1024)
    
    if new_size >= original_size:
        message = (
            f"Сжатие завершено, но размер не уменьшился.\n"
            f"  Исходный: {original_mb:.2f} МБ\n"
            f"  Результат: {new_mb:.2f} МБ\n"
            f"  Пресет: {preset}"
        )
    else:
        message = (
            f"PDF успешно сжат.\n"
            f"  Исходный: {original_mb:.2f} МБ\n"
            f"  Результат: {new_mb:.2f} МБ\n"
            f"  Экономия: {reduction:.1f}%\n"
            f"  Пресет: {preset}"
        )
    
    return OperationResult(
        success=True,
        message=message,
        output_path=output_path,
        files_count=1,
    )
