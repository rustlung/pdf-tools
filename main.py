#!/usr/bin/env python3
"""
PDF Tools CLI - Entry point.

A simple command-line tool for working with PDF files:
- Combine images into PDF
- Extract images from PDF pages
- Compress PDF using Ghostscript

Usage:
    python main.py
"""

import sys

# Ensure Python 3.11+
if sys.version_info < (3, 11):
    print("Требуется Python 3.11 или выше.")
    print(f"Текущая версия: {sys.version}")
    sys.exit(1)


def main() -> None:
    """Application entry point."""
    try:
        from pdfcli.cli.menu import run_menu_loop
        run_menu_loop()
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("\nУбедитесь, что установлены зависимости:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
