"""Operation: Combine images into a single PDF."""

from pathlib import Path

from PIL import Image

from pdfcli.core.config import INPUT_DIR, OUTPUT_DIR, IMAGE_EXTENSIONS
from pdfcli.core.errors import NoFilesError, OperationError
from pdfcli.core.files import list_images
from pdfcli.core.models import ImagesToPdfOptions, OperationResult
from pdfcli.utils.naming import generate_output_name


def images_to_pdf(options: ImagesToPdfOptions | None = None) -> OperationResult:
    """
    Combine images into a single PDF.
    
    If options.image_paths is provided, uses those images in that order.
    Otherwise, uses all images from INPUT_DIR sorted naturally.
    
    Args:
        options: Operation options. Uses defaults if None.
    
    Returns:
        OperationResult with success status and output path.
    
    Raises:
        NoFilesError: If no images found/provided.
        OperationError: If conversion fails.
    """
    options = options or ImagesToPdfOptions()
    
    # Use provided paths or find all images
    if options.image_paths:
        image_paths = options.image_paths
    else:
        image_paths = list_images(INPUT_DIR)
    
    if not image_paths:
        formats = ", ".join(ext.upper().lstrip(".") for ext in sorted(IMAGE_EXTENSIONS))
        raise NoFilesError(
            f"В папке input/ не найдено изображений.\n"
            f"Поддерживаемые форматы: {formats}\n"
            f"Путь: {INPUT_DIR}"
        )
    
    # Prepare output path
    output_name = generate_output_name(options.output_name, extension=".pdf")
    output_path = OUTPUT_DIR / output_name
    
    try:
        # Load and convert all images
        images: list[Image.Image] = []
        
        for img_path in image_paths:
            with Image.open(img_path) as img:
                # Convert to RGB (required for PDF)
                rgb_image = img.convert("RGB")
                # Make a copy since we're in a context manager
                images.append(rgb_image.copy())
        
        if not images:
            raise OperationError("Не удалось загрузить изображения.")
        
        # Save first image with all others appended
        first_image = images[0]
        other_images = images[1:] if len(images) > 1 else []
        
        first_image.save(
            output_path,
            "PDF",
            save_all=True,
            append_images=other_images,
            resolution=100.0,
        )
        
        # Clean up
        for img in images:
            img.close()
        
        return OperationResult(
            success=True,
            message=f"Создан PDF из {len(image_paths)} изображений.",
            output_path=output_path,
            files_count=len(image_paths),
        )
        
    except PermissionError:
        raise OperationError(
            f"Нет прав на запись в {output_path}.\n"
            f"Убедитесь, что файл не открыт в другой программе."
        )
    except Exception as e:
        raise OperationError(f"Ошибка при создании PDF: {e}")
