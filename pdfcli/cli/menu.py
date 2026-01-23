"""Main menu rendering and navigation."""

from pdfcli.core.config import INPUT_DIR, OUTPUT_DIR, ensure_dirs
from pdfcli.core.errors import PDFToolsError, NoFilesError, ToolNotFoundError
from pdfcli.core.files import count_files_summary
from pdfcli.core.models import (
    ImagesToPdfOptions,
    PdfToImagesOptions,
    CompressPdfOptions,
)
from pdfcli.ops.images_to_pdf import images_to_pdf
from pdfcli.ops.pdf_to_images import pdf_to_images
from pdfcli.ops.compress_pdf import compress_pdf
from pdfcli.services.ghostscript import is_ghostscript_available, find_ghostscript
from pdfcli.cli.prompts import (
    prompt_pdf_selection,
    prompt_dpi,
    prompt_image_format,
    prompt_compression_preset,
    prompt_output_name,
    prompt_image_selection,
)
from pdfcli.utils.log import success, error, status


MENU_HEADER = """
╔══════════════════════════════════════════╗
║            PDF TOOLS CLI                 ║
╚══════════════════════════════════════════╝
"""

MENU_OPTIONS = """
  1) Собрать PDF из изображений
  2) Разобрать PDF на изображения
  3) Сжать PDF (Ghostscript)
  4) Выход
"""


def print_separator() -> None:
    """Print a visual separator."""
    print("─" * 44)


def show_startup_status() -> None:
    """Display system status at startup."""
    print(MENU_HEADER)
    print("Статус системы:")
    
    # Check Ghostscript
    gs_path = find_ghostscript()
    if gs_path:
        status("Ghostscript", f"найден ({gs_path})", ok=True)
    else:
        status("Ghostscript", "не найден", ok=False)
    
    # Show directories
    status("Папка input", str(INPUT_DIR), ok=INPUT_DIR.exists())
    status("Папка output", str(OUTPUT_DIR), ok=OUTPUT_DIR.exists())
    
    # Count files
    counts = count_files_summary()
    status("Изображений в input", str(counts["images"]), ok=counts["images"] > 0)
    status("PDF-файлов в input", str(counts["pdfs"]), ok=counts["pdfs"] > 0)
    
    print()


def show_menu() -> None:
    """Display the main menu."""
    print_separator()
    print(MENU_OPTIONS)


def handle_images_to_pdf() -> None:
    """Handle 'images to PDF' operation."""
    print("\n=== Сборка PDF из изображений ===")
    
    # Let user select and order images
    selected_images = prompt_image_selection()
    
    if selected_images is None:
        print("\n  Операция отменена.")
        return
    
    if not selected_images:
        error("Не выбрано ни одного изображения.")
        return
    
    print()
    
    # Get output name
    output_name = prompt_output_name()
    
    print("\n  Обработка...")
    
    try:
        options = ImagesToPdfOptions(
            output_name=output_name,
            image_paths=selected_images,
        )
        result = images_to_pdf(options)
        
        print()
        success(result.message)
        print(f"  Файл: {result.output_path}")
        
    except NoFilesError as e:
        print()
        error(str(e))
    except PDFToolsError as e:
        print()
        error(str(e))


def handle_pdf_to_images() -> None:
    """Handle 'PDF to images' operation."""
    print("\n=== Разбор PDF на изображения ===")
    
    # Select PDF
    pdf_path = prompt_pdf_selection()
    if not pdf_path:
        print("\n  Операция отменена.")
        return
    
    print(f"\n  Выбран: {pdf_path.name}")
    
    # Get options
    dpi = prompt_dpi()
    fmt = prompt_image_format()
    
    print("\n  Обработка...")
    
    try:
        options = PdfToImagesOptions(
            source_pdf=pdf_path,
            dpi=dpi,
            output_format=fmt,
        )
        result = pdf_to_images(options)
        
        print()
        success(result.message)
        print(f"  Папка: {result.output_path}")
        
    except PDFToolsError as e:
        print()
        error(str(e))


def handle_compress_pdf() -> None:
    """Handle 'compress PDF' operation."""
    print("\n=== Сжатие PDF (Ghostscript) ===")
    
    # Check Ghostscript first
    if not is_ghostscript_available():
        print()
        error("Ghostscript не найден в PATH.")
        print("\n  Для использования этой функции установите Ghostscript:")
        print("  Windows: https://ghostscript.com/releases/gsdnld.html")
        print("  Добавьте путь к gswin64c.exe в переменную PATH.")
        print("\n  Проверка: gswin64c --version")
        return
    
    # Select PDF
    pdf_path = prompt_pdf_selection()
    if not pdf_path:
        print("\n  Операция отменена.")
        return
    
    print(f"\n  Выбран: {pdf_path.name}")
    
    # Get preset
    preset = prompt_compression_preset()
    
    print("\n  Сжатие... (может занять время)")
    
    try:
        options = CompressPdfOptions(
            source_pdf=pdf_path,
            preset=preset,
        )
        result = compress_pdf(options)
        
        print()
        success("Готово!")
        print(f"\n{result.message}")
        print(f"\n  Файл: {result.output_path}")
        
    except ToolNotFoundError as e:
        print()
        error(str(e))
    except PDFToolsError as e:
        print()
        error(str(e))


def run_menu_loop() -> None:
    """Run the main menu loop."""
    # Ensure directories exist
    ensure_dirs()
    
    # Show startup status
    show_startup_status()
    
    while True:
        show_menu()
        
        try:
            choice = input("  Выберите действие: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  До свидания!")
            break
        
        if choice == "1":
            handle_images_to_pdf()
        elif choice == "2":
            handle_pdf_to_images()
        elif choice == "3":
            handle_compress_pdf()
        elif choice == "4":
            print("\n  До свидания!")
            break
        else:
            print("\n  Неверный выбор. Введите число от 1 до 4.")
        
        print()
