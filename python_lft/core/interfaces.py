"""Abstract interfaces for Python LFT tools."""

from abc import ABC, abstractmethod
from typing import Optional

from .models import CommandResult, ToolConfig


class ToolExecutor(ABC):
    """Abstract base class for tool execution."""

    @abstractmethod
    async def execute(self, files: list[str], **kwargs) -> CommandResult:
        """Execute the tool on the given files."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the tool name."""
        pass

    @property
    @abstractmethod
    def command(self) -> str:
        """Get the tool command."""
        pass


class LinterExecutor(ToolExecutor):
    """Abstract base class for linter tools."""

    @abstractmethod
    async def lint(self, files: list[str]) -> CommandResult:
        """Execute linting on files."""
        pass

    async def execute(self, files: list[str], **kwargs) -> CommandResult:
        """Execute linting."""
        return await self.lint(files)


class FormatterExecutor(ToolExecutor):
    """Abstract base class for formatter tools."""

    @abstractmethod
    async def format(self, files: list[str], line_length: int = 88) -> CommandResult:
        """Execute formatting on files."""
        pass

    async def execute(self, files: list[str], **kwargs) -> CommandResult:
        """Execute formatting."""
        line_length = kwargs.get("line_length", 88)
        return await self.format(files, line_length)


class TesterExecutor(ToolExecutor):
    """Abstract base class for test runner tools."""

    @abstractmethod
    async def test(self, target: str) -> CommandResult:
        """Execute tests."""
        pass

    async def execute(self, files: list[str], **kwargs) -> CommandResult:
        """Execute testing."""
        target = kwargs.get("target", "all")
        return await self.test(target)


class ToolFactory(ABC):
    """Abstract factory for creating tool executors."""

    @abstractmethod
    def create_executor(self, tool_config: ToolConfig) -> Optional[ToolExecutor]:
        """Create a tool executor from configuration."""
        pass

    @abstractmethod
    def get_supported_tools(self) -> list[str]:
        """Get list of supported tool names."""
        pass


class ResultFormatter(ABC):
    """Abstract base class for formatting tool results."""

    @abstractmethod
    def format_success(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format a successful result."""
        pass

    @abstractmethod
    def format_warning(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format a warning result."""
        pass

    @abstractmethod
    def format_error(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format an error result."""
        pass
