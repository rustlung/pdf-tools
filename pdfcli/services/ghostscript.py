"""Ghostscript service: detection and command execution."""

import shutil
import subprocess
from pathlib import Path
from typing import Literal

from pdfcli.core.errors import ToolNotFoundError, OperationError


# Possible Ghostscript binary names
GS_BINARIES = ["gs", "gswin64c", "gswin32c"]


def find_ghostscript() -> str | None:
    """
    Find Ghostscript binary in PATH.
    
    Checks for 'gs' first, then Windows-specific names.
    
    Returns:
        Path to Ghostscript binary, or None if not found.
    """
    for binary in GS_BINARIES:
        path = shutil.which(binary)
        if path:
            return path
    return None


def is_ghostscript_available() -> bool:
    """Check if Ghostscript is available."""
    return find_ghostscript() is not None


def get_ghostscript_install_hint() -> str:
    """Return installation instructions for Ghostscript."""
    return (
        "Ghostscript не найден в PATH.\n"
        "Для установки:\n"
        "  Windows: скачайте с https://ghostscript.com/releases/gsdnld.html\n"
        "           и добавьте путь к gswin64c.exe в переменную PATH.\n"
        "  Linux:   sudo apt install ghostscript\n"
        "  macOS:   brew install ghostscript\n"
        "\nПроверка: выполните 'gs --version' или 'gswin64c --version' в терминале."
    )


def build_compress_command(
    gs_binary: str,
    input_path: Path,
    output_path: Path,
    preset: Literal["screen", "ebook", "printer", "prepress"] = "ebook"
) -> list[str]:
    """
    Build Ghostscript compression command.
    
    Args:
        gs_binary: Path to Ghostscript binary.
        input_path: Input PDF path.
        output_path: Output PDF path.
        preset: Compression preset.
    
    Returns:
        Command as list of strings.
    """
    return [
        gs_binary,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{preset}",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        f"-sOutputFile={output_path}",
        str(input_path),
    ]


def run_ghostscript(
    input_path: Path,
    output_path: Path,
    preset: Literal["screen", "ebook", "printer", "prepress"] = "ebook"
) -> None:
    """
    Run Ghostscript to compress PDF.
    
    Args:
        input_path: Input PDF path.
        output_path: Output PDF path.
        preset: Compression preset.
    
    Raises:
        ToolNotFoundError: If Ghostscript is not found.
        OperationError: If Ghostscript returns an error.
    """
    gs_binary = find_ghostscript()
    
    if not gs_binary:
        raise ToolNotFoundError(get_ghostscript_install_hint())
    
    command = build_compress_command(gs_binary, input_path, output_path, preset)
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            raise OperationError(
                f"Ghostscript завершился с ошибкой (код {result.returncode}):\n{error_msg}"
            )
            
    except FileNotFoundError:
        raise ToolNotFoundError(get_ghostscript_install_hint())
    except subprocess.SubprocessError as e:
        raise OperationError(f"Ошибка запуска Ghostscript: {e}")
