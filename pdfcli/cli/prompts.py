"""User input prompts and validation."""

from pathlib import Path
from typing import Literal

from pdfcli.core.files import list_pdfs, list_images
from pdfcli.core.config import INPUT_DIR, IMAGE_EXTENSIONS

# Confirmation values for yes/no prompts
_YES_VALUES = ("", "y", "yes", "д", "да")


def prompt_confirm(message: str, default_yes: bool = True) -> bool:
    """
    Prompt user for yes/no confirmation.
    
    Args:
        message: Prompt message.
        default_yes: If True, empty input means yes.
    
    Returns:
        True if confirmed, False otherwise.
    """
    hint = "[Y/n]" if default_yes else "[y/N]"
    raw = input(f"{message} {hint}: ").strip().lower()
    
    if default_yes:
        return raw in _YES_VALUES
    else:
        return raw in ("y", "yes", "д", "да")


def prompt_int(
    message: str,
    default: int | None = None,
    min_val: int | None = None,
    max_val: int | None = None,
) -> int:
    """
    Prompt user for an integer value.
    
    Args:
        message: Prompt message.
        default: Default value if user presses Enter.
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.
    
    Returns:
        User input as integer.
    """
    default_str = f" [{default}]" if default is not None else ""
    
    while True:
        try:
            raw = input(f"{message}{default_str}: ").strip()
            
            if not raw and default is not None:
                return default
            
            value = int(raw)
            
            if min_val is not None and value < min_val:
                print(f"  Значение должно быть >= {min_val}")
                continue
            
            if max_val is not None and value > max_val:
                print(f"  Значение должно быть <= {max_val}")
                continue
            
            return value
            
        except ValueError:
            print("  Введите целое число.")


def prompt_choice(
    message: str,
    choices: list[str],
    default: str | None = None,
) -> str:
    """
    Prompt user to select from a list of choices.
    
    Args:
        message: Prompt message.
        choices: List of valid choices.
        default: Default choice if user presses Enter.
    
    Returns:
        Selected choice.
    """
    choices_str = "/".join(choices)
    default_str = f" [{default}]" if default else ""
    
    while True:
        raw = input(f"{message} ({choices_str}){default_str}: ").strip().lower()
        
        if not raw and default:
            return default
        
        if raw in choices:
            return raw
        
        print(f"  Выберите один из вариантов: {choices_str}")


def prompt_pdf_selection() -> Path | None:
    """
    Show list of PDFs in INPUT_DIR and let user select one.
    
    Returns:
        Path to selected PDF, or None if no PDFs or cancelled.
    """
    pdfs = list_pdfs()
    
    if not pdfs:
        print(f"\n  В папке input/ нет PDF-файлов.")
        print(f"  Путь: {INPUT_DIR}")
        return None
    
    if len(pdfs) == 1:
        print(f"\n  Найден один PDF: {pdfs[0].name}")
        if prompt_confirm("  Использовать его?"):
            return pdfs[0]
        return None
    
    # Multiple PDFs - show numbered list
    print(f"\n  Найдено PDF-файлов: {len(pdfs)}")
    print("  " + "-" * 40)
    
    for i, pdf in enumerate(pdfs, 1):
        size_mb = pdf.stat().st_size / (1024 * 1024)
        print(f"  {i}) {pdf.name} ({size_mb:.2f} МБ)")
    
    print("  " + "-" * 40)
    print("  0) Отмена")
    print()
    
    choice = prompt_int("  Выберите номер", min_val=0, max_val=len(pdfs))
    
    if choice == 0:
        return None
    
    return pdfs[choice - 1]


def prompt_dpi(default: int = 150) -> int:
    """Prompt for DPI value."""
    return prompt_int(
        "  DPI (разрешение)",
        default=default,
        min_val=72,
        max_val=600,
    )


def prompt_image_format(default: str = "png") -> Literal["png", "jpg"]:
    """Prompt for output image format."""
    choice = prompt_choice(
        "  Формат изображений",
        choices=["png", "jpg"],
        default=default,
    )
    return "jpg" if choice == "jpg" else "png"


def prompt_compression_preset(
    default: str = "ebook"
) -> Literal["screen", "ebook", "printer", "prepress"]:
    """
    Prompt for Ghostscript compression preset.
    
    Presets (from lowest to highest quality):
    - screen: 72 dpi, lowest quality, smallest size
    - ebook: 150 dpi, good for ebook readers
    - printer: 300 dpi, good for printing
    - prepress: 300 dpi, highest quality, largest size
    """
    print("\n  Пресеты сжатия:")
    print("    screen   - низкое качество (72 dpi), минимальный размер")
    print("    ebook    - среднее качество (150 dpi), для чтения")
    print("    printer  - высокое качество (300 dpi), для печати")
    print("    prepress - максимальное качество, минимальное сжатие")
    print()
    
    choice = prompt_choice(
        "  Выберите пресет",
        choices=["screen", "ebook", "printer", "prepress"],
        default=default,
    )
    
    # Type narrowing
    if choice == "screen":
        return "screen"
    elif choice == "printer":
        return "printer"
    elif choice == "prepress":
        return "prepress"
    else:
        return "ebook"


def prompt_output_name(default: str = "combined") -> str:
    """Prompt for output PDF name."""
    default_str = f" [{default}]"
    
    while True:
        raw = input(f"  Имя выходного файла (без .pdf){default_str}: ").strip()
        
        if not raw:
            return default
        
        # Basic validation
        if any(c in raw for c in '<>:"/\\|?*'):
            print("  Имя содержит недопустимые символы.")
            continue
        
        return raw


def prompt_image_selection() -> list[Path] | None:
    """
    Show list of images in INPUT_DIR and let user select which ones to include.
    User can specify order by entering numbers in desired sequence.
    
    Returns:
        List of selected image paths in user-specified order, or None if cancelled.
    """
    images = list_images()
    
    if not images:
        formats = ", ".join(ext.upper().lstrip(".") for ext in sorted(IMAGE_EXTENSIONS))
        print(f"\n  В папке input/ нет изображений.")
        print(f"  Поддерживаемые форматы: {formats}")
        print(f"  Путь: {INPUT_DIR}")
        return None
    
    # Show numbered list of all images
    print(f"\n  Найдено изображений: {len(images)}")
    print("  " + "-" * 50)
    
    for i, img in enumerate(images, 1):
        size_kb = img.stat().st_size / 1024
        print(f"  {i:3}) {img.name} ({size_kb:.1f} КБ)")
    
    print("  " + "-" * 50)
    print()
    print("  Варианты ввода:")
    print("    * (или Enter) - использовать все файлы в текущем порядке")
    print("    1 3 5         - выбрать файлы 1, 3, 5 в указанном порядке")
    print("    1-5           - выбрать файлы с 1 по 5")
    print("    1-3 7 9-11    - комбинация диапазонов и отдельных номеров")
    print("    0             - отмена")
    print()
    
    while True:
        raw = input("  Введите номера файлов: ").strip()
        
        # Empty or * means all files in current order
        if raw == "" or raw == "*":
            return images
        
        # 0 means cancel
        if raw == "0":
            return None
        
        # Parse input
        try:
            selected_indices = _parse_number_selection(raw, len(images))
        except _ParseError as e:
            print(f"  {e}")
            continue
        
        if not selected_indices:
            print("  Не выбрано ни одного файла.")
            continue
        
        # Map indices to paths
        selected_paths = [images[i] for i in selected_indices]
        
        # Show selected order
        print(f"\n  Выбрано файлов: {len(selected_paths)}")
        print("  Порядок в PDF:")
        for i, path in enumerate(selected_paths, 1):
            print(f"    {i}. {path.name}")
        
        if prompt_confirm("\n  Подтвердить?"):
            return selected_paths
        
        print()  # Continue loop for re-selection


class _ParseError(Exception):
    """Internal error for number parsing with user-friendly message."""
    pass


def _parse_number_selection(raw: str, max_num: int) -> list[int]:
    """
    Parse user input for number selection.
    
    Supports:
    - Single numbers: "1 3 5"
    - Ranges: "1-5"
    - Mixed: "1-3 7 9-11"
    
    Args:
        raw: User input string.
        max_num: Maximum valid number (1-indexed).
    
    Returns:
        List of 0-indexed positions.
    
    Raises:
        _ParseError: If parsing failed, with user-friendly message.
    """
    indices: list[int] = []
    parts = raw.split()
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Check for range (e.g., "1-5")
        if "-" in part:
            range_parts = part.split("-")
            if len(range_parts) != 2:
                raise _ParseError("Неверный формат диапазона. Используйте: 1-5")
            
            try:
                start = int(range_parts[0])
                end = int(range_parts[1])
            except ValueError:
                raise _ParseError("Диапазон должен содержать числа: 1-5")
            
            if start < 1 or end < 1 or start > max_num or end > max_num:
                raise _ParseError(f"Номера должны быть от 1 до {max_num}.")
            
            if start > end:
                # Allow reverse ranges
                indices.extend(range(start - 1, end - 2, -1))
            else:
                indices.extend(range(start - 1, end))
        else:
            # Single number
            try:
                num = int(part)
            except ValueError:
                raise _ParseError(f"'{part}' — не число.")
            
            if num < 1 or num > max_num:
                raise _ParseError(f"Номер {num} вне диапазона (1-{max_num}).")
            
            indices.append(num - 1)
    
    return indices
