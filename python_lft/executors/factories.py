"""Factory classes for creating tool executors."""

from typing import ClassVar, Optional

from ..core.interfaces import (
    FormatterExecutor,
    LinterExecutor,
    TesterExecutor,
    ToolFactory,
)
from ..core.models import ToolConfig
from .formatters import (
    Autopep8Formatter,
    BlackFormatter,
    IsortFormatter,
    RuffFormatter,
    YapfFormatter,
)
from .linters import BanditLinter, Flake8Linter, MyPyLinter, PylintLinter, RuffLinter
from .testers import Nose2Tester, PytestTester, UnittestTester


class LinterFactory(ToolFactory):
    """Factory for creating linter executors."""

    _LINTER_CLASSES: ClassVar[dict[str, type[LinterExecutor]]] = {
        "ruff": RuffLinter,
        "flake8": Flake8Linter,
        "pylint": PylintLinter,
        "mypy": MyPyLinter,
        "bandit": BanditLinter,
    }

    def create_executor(self, tool_config: ToolConfig) -> Optional[LinterExecutor]:
        """Create a linter executor from configuration."""
        if not tool_config.available:
            return None

        linter_class = self._LINTER_CLASSES.get(tool_config.name)
        if linter_class:
            return linter_class(tool_config.command)

        return None

    def get_supported_tools(self) -> list[str]:
        """Get list of supported linter names."""
        return list(self._LINTER_CLASSES.keys())


class FormatterFactory(ToolFactory):
    """Factory for creating formatter executors."""

    _FORMATTER_CLASSES: ClassVar[dict[str, type[FormatterExecutor]]] = {
        "black": BlackFormatter,
        "ruff": RuffFormatter,
        "isort": IsortFormatter,
        "autopep8": Autopep8Formatter,
        "yapf": YapfFormatter,
    }

    def create_executor(self, tool_config: ToolConfig) -> Optional[FormatterExecutor]:
        """Create a formatter executor from configuration."""
        if not tool_config.available:
            return None

        formatter_class = self._FORMATTER_CLASSES.get(tool_config.name)
        if formatter_class:
            return formatter_class(tool_config.command)

        return None

    def get_supported_tools(self) -> list[str]:
        """Get list of supported formatter names."""
        return list(self._FORMATTER_CLASSES.keys())


class TesterFactory(ToolFactory):
    """Factory for creating test runner executors."""

    _TESTER_CLASSES: ClassVar[dict[str, type[TesterExecutor]]] = {
        "pytest": PytestTester,
        "nose2": Nose2Tester,
        "unittest": UnittestTester,
    }

    def create_executor(self, tool_config: ToolConfig) -> Optional[TesterExecutor]:
        """Create a test runner executor from configuration."""
        if not tool_config.available:
            return None

        tester_class = self._TESTER_CLASSES.get(tool_config.name)
        if tester_class:
            return tester_class(tool_config.command)

        return None

    def get_supported_tools(self) -> list[str]:
        """Get list of supported test runner names."""
        return list(self._TESTER_CLASSES.keys())
