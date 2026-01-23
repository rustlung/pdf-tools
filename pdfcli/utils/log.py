"""Simple logging utilities for console output."""

import sys
from typing import TextIO


def info(message: str, file: TextIO = sys.stdout) -> None:
    """Print info message."""
    print(f"[INFO] {message}", file=file)


def success(message: str, file: TextIO = sys.stdout) -> None:
    """Print success message."""
    print(f"[OK] {message}", file=file)


def warn(message: str, file: TextIO = sys.stderr) -> None:
    """Print warning message."""
    print(f"[WARN] {message}", file=file)


def error(message: str, file: TextIO = sys.stderr) -> None:
    """Print error message."""
    print(f"[ERROR] {message}", file=file)


def status(label: str, value: str, ok: bool = True) -> None:
    """Print status line with label and value."""
    marker = "+" if ok else "-"
    print(f"  [{marker}] {label}: {value}")
