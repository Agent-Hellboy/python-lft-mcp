"""Core data models for Python LFT."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class ToolStatus(Enum):
    """Tool execution status."""

    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class CommandResult:
    """Result of running a subprocess command."""

    exit_code: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        """True if command succeeded (exit code 0)."""
        return self.exit_code == 0

    @property
    def output(self) -> str:
        """Combined stdout and stderr."""
        return (self.stdout + self.stderr).strip()


@dataclass
class ToolConfig:
    """Configuration for a detected tool."""

    name: str
    command: str
    available: bool
    config_files: list[str]
    config_data: Optional[dict[str, Any]] = None


@dataclass
class WorkspaceTools:
    """Detected tools in the workspace."""

    linters: list[ToolConfig]
    formatters: list[ToolConfig]
    testers: list[ToolConfig]
    config_files: dict[str, bool]

    def get_best_linter(self) -> Optional[ToolConfig]:
        """Get the highest priority available linter."""
        return next((tool for tool in self.linters if tool.available), None)

    def get_best_formatter(self) -> Optional[ToolConfig]:
        """Get the highest priority available formatter."""
        return next((tool for tool in self.formatters if tool.available), None)

    def get_best_tester(self) -> Optional[ToolConfig]:
        """Get the highest priority available tester."""
        return next((tool for tool in self.testers if tool.available), None)


@dataclass
class ToolResult:
    """Result of tool execution."""

    tool_name: str
    status: ToolStatus
    message: str
    details: Optional[str] = None
    files_processed: int = 0
    files_changed: int = 0
    issues_found: int = 0
    tests_run: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
