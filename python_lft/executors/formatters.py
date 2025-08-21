"""Formatter executor implementations."""

from ..config.constants import QUICK_TIMEOUT
from ..core.interfaces import FormatterExecutor
from ..core.models import CommandResult
from ..services.runners import run as run_command


class BlackFormatter(FormatterExecutor):
    """Black formatter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "black"

    @property
    def command(self) -> str:
        return self._command

    async def format(self, files: list[str], line_length: int = 88) -> CommandResult:
        """Execute black formatting."""
        cmd = [self._command, "--line-length", str(line_length), *files]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)


class RuffFormatter(FormatterExecutor):
    """Ruff formatter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "ruff"

    @property
    def command(self) -> str:
        return self._command

    async def format(self, files: list[str], line_length: int = 88) -> CommandResult:
        """Execute ruff formatting."""
        cmd = [self._command, "format", "--line-length", str(line_length), *files]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)


class IsortFormatter(FormatterExecutor):
    """Isort formatter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "isort"

    @property
    def command(self) -> str:
        return self._command

    async def format(self, files: list[str], line_length: int = 88) -> CommandResult:
        """Execute isort formatting."""
        cmd = [self._command, "--line-length", str(line_length), *files]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)


class Autopep8Formatter(FormatterExecutor):
    """Autopep8 formatter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "autopep8"

    @property
    def command(self) -> str:
        return self._command

    async def format(self, files: list[str], line_length: int = 88) -> CommandResult:
        """Execute autopep8 formatting."""
        cmd = [
            self._command,
            "--in-place",
            "--max-line-length",
            str(line_length),
            *files,
        ]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)


class YapfFormatter(FormatterExecutor):
    """YAPF formatter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "yapf"

    @property
    def command(self) -> str:
        return self._command

    async def format(self, files: list[str], line_length: int = 88) -> CommandResult:
        """Execute yapf formatting."""
        cmd = [
            self._command,
            "--in-place",
            f"--style={{column_limit: {line_length}}}",
            *files,
        ]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)
