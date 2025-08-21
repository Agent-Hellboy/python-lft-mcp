"""Test runner executor implementations."""

from ..config.constants import DEFAULT_TIMEOUT
from ..core.interfaces import TesterExecutor
from ..core.models import CommandResult
from ..services.runners import run as run_command


class PytestTester(TesterExecutor):
    """Pytest test runner executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "pytest"

    @property
    def command(self) -> str:
        return self._command

    async def test(self, target: str) -> CommandResult:
        """Execute pytest tests."""
        base_args = ["--maxfail=1", "--disable-warnings"]

        if target == "all":
            cmd = [self._command, *base_args]
        else:
            cmd = [self._command, *base_args, target]

        return await run_command(cmd, timeout=DEFAULT_TIMEOUT)


class Nose2Tester(TesterExecutor):
    """Nose2 test runner executor."""

    def __init__(self, command: str):
        self._command = command

    @property
    def name(self) -> str:
        return "nose2"

    @property
    def command(self) -> str:
        return self._command

    async def test(self, target: str) -> CommandResult:
        """Execute nose2 tests."""
        if target == "all":
            cmd = [self._command]
        else:
            cmd = [self._command, target]

        return await run_command(cmd, timeout=DEFAULT_TIMEOUT)


class UnittestTester(TesterExecutor):
    """Unittest test runner executor."""

    def __init__(self, command: str = "python"):
        self._command = command

    @property
    def name(self) -> str:
        return "unittest"

    @property
    def command(self) -> str:
        return self._command

    async def test(self, target: str) -> CommandResult:
        """Execute unittest tests."""
        if target == "all":
            # Use discovery for all tests
            cmd = [
                self._command,
                "-m",
                "unittest",
                "discover",
                "-s",
                ".",
                "-p",
                "*test*.py",
            ]
        else:
            # Run specific test module/file
            if target.endswith(".py"):
                # Convert file path to module path
                module_path = target.replace("/", ".").replace(".py", "")
                cmd = [self._command, "-m", "unittest", module_path]
            else:
                cmd = [self._command, "-m", "unittest", target]

        return await run_command(cmd, timeout=DEFAULT_TIMEOUT)
