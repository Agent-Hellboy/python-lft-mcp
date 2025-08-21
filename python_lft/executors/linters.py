"""Linter executor implementations."""

from ..config.constants import QUICK_TIMEOUT
from ..core.interfaces import LinterExecutor
from ..core.models import CommandResult
from ..services.runners import run as run_command


class RuffLinter(LinterExecutor):
    """Ruff linter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "ruff"

    @property
    def command(self) -> str:
        return self._command

    async def lint(self, files: list[str]) -> CommandResult:
        """Execute ruff linting."""
        cmd = [self._command, "check", *files]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)


class Flake8Linter(LinterExecutor):
    """Flake8 linter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "flake8"

    @property
    def command(self) -> str:
        return self._command

    async def lint(self, files: list[str]) -> CommandResult:
        """Execute flake8 linting."""
        cmd = [self._command, *files]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)


class PylintLinter(LinterExecutor):
    """Pylint linter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "pylint"

    @property
    def command(self) -> str:
        return self._command

    async def lint(self, files: list[str]) -> CommandResult:
        """Execute pylint linting."""
        cmd = [self._command, *files]
        return await run_command(cmd, timeout=QUICK_TIMEOUT * 2)


class MyPyLinter(LinterExecutor):
    """MyPy linter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "mypy"

    @property
    def command(self) -> str:
        return self._command

    async def lint(self, files: list[str]) -> CommandResult:
        """Execute mypy linting."""
        cmd = [self._command, *files]
        return await run_command(cmd, timeout=QUICK_TIMEOUT * 2)


class BanditLinter(LinterExecutor):
    """Bandit security linter executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "bandit"

    @property
    def command(self) -> str:
        return self._command

    async def lint(self, files: list[str]) -> CommandResult:
        """Execute bandit security linting."""
        # Bandit works better with recursive scanning
        import os

        config_args = []
        for config_file in [
            ".bandit",
            "bandit.yaml",
            "bandit.yml",
            ".bandit.yaml",
            ".bandit.yml",
        ]:
            if os.path.exists(config_file):
                config_args = ["-c", config_file]
                break

        cmd = [self._command, *config_args, "-r", "."]
        return await run_command(cmd, timeout=QUICK_TIMEOUT)
