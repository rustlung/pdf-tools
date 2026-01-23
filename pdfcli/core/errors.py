"""Custom exceptions for PDF Tools."""


class PDFToolsError(Exception):
    """Base exception for PDF Tools."""
    pass


class UserError(PDFToolsError):
    """Error caused by user input or missing files."""
    pass


class ToolNotFoundError(PDFToolsError):
    """External tool (like Ghostscript) not found."""
    pass


class OperationError(PDFToolsError):
    """Error during operation execution."""
    pass


class NoFilesError(UserError):
    """No files found for operation."""
    pass
