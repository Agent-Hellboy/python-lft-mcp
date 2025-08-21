"""Result formatting implementations."""

from typing import Optional

from .interfaces import ResultFormatter


class StandardFormatter(ResultFormatter):
    """Standard text formatter without emojis."""

    def format_success(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format a successful result."""
        result = f"[SUCCESS] {tool_name}: {message}"
        if details and details.strip():
            result += f"\n\n{details}"
        return result

    def format_warning(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format a warning result."""
        result = f"[WARNING] {tool_name}: {message}"
        if details and details.strip():
            result += f"\n\n{details}"
        return result

    def format_error(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format an error result."""
        result = f"[ERROR] {tool_name}: {message}"
        if details and details.strip():
            result += f"\n\n{details}"
        return result


class CompactFormatter(ResultFormatter):
    """Compact formatter for brief output."""

    def format_success(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format a successful result."""
        return f"OK: {tool_name} - {message}"

    def format_warning(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format a warning result."""
        return f"WARN: {tool_name} - {message}"

    def format_error(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format an error result."""
        return f"ERROR: {tool_name} - {message}"
