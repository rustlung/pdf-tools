"""Operation: Extract images from PDF pages."""

from pathlib import Path
from typing import Literal

import fitz  # PyMuPDF

from pdfcli.core.config import OUTPUT_DIR
from pdfcli.core.errors import OperationError
from pdfcli.core.models import PdfToImagesOptions, OperationResult
from pdfcli.utils.naming import sanitize_filename, format_page_number


def pdf_to_images(options: PdfToImagesOptions) -> OperationResult:
    """
    Extract each page of a PDF as an image.
    
    Creates a subdirectory in OUTPUT_DIR named after the PDF file.
    
    Args:
        options: Operation options including source PDF, DPI, and format.
    
    Returns:
        OperationResult with success status and output directory.
    
    Raises:
        OperationError: If extraction fails.
    """
    source_pdf = options.source_pdf
    dpi = options.dpi
    output_format = options.output_format
    
    # Validate source
    if not source_pdf.exists():
        raise OperationError(f"Файл не найден: {source_pdf}")
    
    # Create output subdirectory
    safe_name = sanitize_filename(source_pdf.stem)
    output_dir = OUTPUT_DIR / safe_name
    output_dir.mkdir(exist_ok=True)
    
    # Calculate zoom factor from DPI (72 is PDF base DPI)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    
    # Determine image format settings
    if output_format == "jpg":
        extension = ".jpg"
        # For JPEG output in PyMuPDF
        pix_format = "jpeg"
    else:
        extension = ".png"
        pix_format = "png"
    
    try:
        doc = fitz.open(source_pdf)
        total_pages = len(doc)
        
        if total_pages == 0:
            doc.close()
            raise OperationError(f"PDF пустой: {source_pdf.name}")
        
        saved_count = 0
        
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=matrix)
            
            # Generate filename with leading zeros
            page_str = format_page_number(page_num + 1, total_pages)
            filename = f"page_{page_str}{extension}"
            output_path = output_dir / filename
            
            # Save image
            if output_format == "jpg":
                pix.save(output_path, output=pix_format, jpg_quality=95)
            else:
                pix.save(output_path, output=pix_format)
            
            saved_count += 1
        
        doc.close()
        
        return OperationResult(
            success=True,
            message=f"Извлечено {saved_count} страниц в формате {output_format.upper()} ({dpi} DPI).",
            output_path=output_dir,
            files_count=saved_count,
        )
        
    except fitz.FileDataError:
        raise OperationError(
            f"Не удалось открыть PDF: {source_pdf.name}\n"
            f"Файл может быть повреждён или защищён паролем."
        )
    except PermissionError:
        raise OperationError(
            f"Нет прав на запись в {output_dir}.\n"
            f"Убедитесь, что папка не используется другой программой."
        )
    except Exception as e:
        raise OperationError(f"Ошибка при извлечении страниц: {e}")
