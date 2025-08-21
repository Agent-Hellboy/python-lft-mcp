"""Service orchestrator using strategy pattern for tool execution."""

import logging
from typing import Optional

from ..config.constants import MAX_FILES_PER_BATCH
from ..core.config import get_config_manager
from ..core.interfaces import (
    FormatterExecutor,
    LinterExecutor,
    TesterExecutor,
)
from ..executors.factories import FormatterFactory, LinterFactory, TesterFactory
from ..services.runners import combine_results, run_chunked
from ..services.workspace import detect_tools, get_python_files


logger = logging.getLogger(__name__)


class ToolOrchestrator:
    """Orchestrates tool execution using strategy pattern."""

    def __init__(self):
        self._linter_factory = LinterFactory()
        self._formatter_factory = FormatterFactory()
        self._tester_factory = TesterFactory()
        self._config_manager = get_config_manager()

    async def lint(
        self,
        target: str = "all",
        preferred_tool: Optional[str] = None,
        work_dir: Optional[str] = None,
    ) -> str:
        """Execute linting using strategy pattern."""
        logger.info(
            f"Orchestrating lint operation: target={target}, preferred_tool={preferred_tool}, work_dir={work_dir}"
        )

        # Get files to lint
        files = get_python_files(target, work_dir=work_dir)
        if not files:
            return self._format_warning("lint", "No Python files found to lint")

        # Get linter executor
        executor = self._get_linter_executor(preferred_tool, work_dir=work_dir)
        if not executor:
            available_tools = self._get_available_linters(work_dir=work_dir)
            if not available_tools:
                return self._format_error(
                    "lint",
                    "No linter available",
                    "Install one of: ruff, flake8, pylint, mypy, bandit",
                )
            else:
                return self._format_error(
                    "lint",
                    f"Requested linter '{preferred_tool}' not available",
                    f"Available linters: {', '.join(available_tools)}",
                )

        # Execute linting
        try:
            if len(files) > MAX_FILES_PER_BATCH:
                # Use chunked execution for large file sets
                results = await run_chunked(
                    [executor.command, "check"]
                    if executor.name == "ruff"
                    else [executor.command],
                    files,
                    chunk_size=MAX_FILES_PER_BATCH,
                )
                result = combine_results(results)
            else:
                result = await executor.execute(files)

            # Format and return result
            if result.success:
                if result.exit_code == 0:
                    return self._format_success(
                        executor.name,
                        f"{len(files)} files checked, no issues found",
                        result.output if result.output.strip() else None,
                    )
                else:
                    return self._format_warning(
                        executor.name,
                        f"{len(files)} files checked, issues found",
                        result.output,
                    )
            else:
                return self._format_error(
                    executor.name, "Linting failed", result.output
                )

        except Exception as e:
            logger.error(f"Linting failed: {e}")
            return self._format_error(executor.name, "Linting failed", str(e))

    async def format(
        self,
        target: str = "all",
        line_length: int = 88,
        preferred_tool: Optional[str] = None,
        work_dir: Optional[str] = None,
    ) -> str:
        """Execute formatting using strategy pattern."""
        logger.info(
            f"Orchestrating format operation: target={target}, line_length={line_length}, preferred_tool={preferred_tool}, work_dir={work_dir}"
        )

        # Get files to format
        files = get_python_files(target, work_dir=work_dir)
        if not files:
            return self._format_warning("format", "No Python files found to format")

        # Get formatter executor
        executor = self._get_formatter_executor(preferred_tool, work_dir=work_dir)
        if not executor:
            available_tools = self._get_available_formatters(work_dir=work_dir)
            if not available_tools:
                return self._format_error(
                    "format",
                    "No formatter available",
                    "Install one of: black, ruff, isort, autopep8, yapf",
                )
            else:
                return self._format_error(
                    "format",
                    f"Requested formatter '{preferred_tool}' not available",
                    f"Available formatters: {', '.join(available_tools)}",
                )

        # Execute formatting
        try:
            result = await executor.execute(files, line_length=line_length)

            # Parse formatter-specific output for change detection
            files_changed = self._count_formatted_files(executor.name, result.output)

            if result.success:
                if files_changed > 0:
                    return self._format_success(
                        executor.name,
                        f"{len(files)} files processed, {files_changed} files changed",
                        result.output if result.output.strip() else None,
                    )
                else:
                    return self._format_success(
                        executor.name,
                        f"{len(files)} files processed, no changes needed",
                    )
            else:
                return self._format_error(
                    executor.name, "Formatting failed", result.output
                )

        except Exception as e:
            logger.error(f"Formatting failed: {e}")
            return self._format_error(executor.name, "Formatting failed", str(e))

    async def test(
        self,
        target: str = "all",
        preferred_tool: Optional[str] = None,
        work_dir: Optional[str] = None,
    ) -> str:
        """Execute testing using strategy pattern."""
        logger.info(
            f"Orchestrating test operation: target={target}, preferred_tool={preferred_tool}, work_dir={work_dir}"
        )

        # Get tester executor
        executor = self._get_tester_executor(preferred_tool, work_dir=work_dir)
        if not executor:
            available_tools = self._get_available_testers(work_dir=work_dir)
            if not available_tools:
                return self._format_error(
                    "test",
                    "No test runner available",
                    "Install one of: pytest, nose2, or use unittest",
                )
            else:
                return self._format_error(
                    "test",
                    f"Requested test runner '{preferred_tool}' not available",
                    f"Available test runners: {', '.join(available_tools)}",
                )

        # Execute testing
        try:
            result = await executor.execute([], target=target)

            # Parse test results
            tests_run, tests_passed, tests_failed = self._parse_test_output(
                executor.name, result.output
            )

            if result.success and tests_failed == 0:
                if tests_run > 0:
                    return self._format_success(
                        executor.name, f"{tests_run} tests run, all passed"
                    )
                else:
                    return self._format_warning(executor.name, "No tests found")
            else:
                if tests_failed > 0:
                    return self._format_error(
                        executor.name,
                        f"{tests_run} tests run, {tests_failed} failed",
                        result.output,
                    )
                else:
                    return self._format_error(
                        executor.name, "Test execution failed", result.output
                    )

        except Exception as e:
            logger.error(f"Testing failed: {e}")
            return self._format_error(executor.name, "Testing failed", str(e))

    def _get_linter_executor(
        self, preferred_tool: Optional[str], work_dir: Optional[str] = None
    ) -> Optional[LinterExecutor]:
        """Get linter executor based on preference or auto-detection."""
        workspace_tools = detect_tools(work_dir=work_dir)

        if preferred_tool:
            # Find specific tool
            for tool_config in workspace_tools.linters:
                if tool_config.name == preferred_tool and tool_config.available:
                    return self._linter_factory.create_executor(tool_config)
        else:
            # Use best available
            best_tool = workspace_tools.get_best_linter()
            if best_tool:
                return self._linter_factory.create_executor(best_tool)

        return None

    def _get_formatter_executor(
        self, preferred_tool: Optional[str], work_dir: Optional[str] = None
    ) -> Optional[FormatterExecutor]:
        """Get formatter executor based on preference or auto-detection."""
        workspace_tools = detect_tools(work_dir=work_dir)

        if preferred_tool:
            # Find specific tool
            for tool_config in workspace_tools.formatters:
                if tool_config.name == preferred_tool and tool_config.available:
                    return self._formatter_factory.create_executor(tool_config)
        else:
            # Use best available
            best_tool = workspace_tools.get_best_formatter()
            if best_tool:
                return self._formatter_factory.create_executor(best_tool)

        return None

    def _get_tester_executor(
        self, preferred_tool: Optional[str], work_dir: Optional[str] = None
    ) -> Optional[TesterExecutor]:
        """Get tester executor based on preference or auto-detection."""
        workspace_tools = detect_tools(work_dir=work_dir)

        if preferred_tool:
            # Find specific tool
            for tool_config in workspace_tools.testers:
                if tool_config.name == preferred_tool and tool_config.available:
                    return self._tester_factory.create_executor(tool_config)
        else:
            # Use best available
            best_tool = workspace_tools.get_best_tester()
            if best_tool:
                return self._tester_factory.create_executor(best_tool)

        return None

    def _get_available_linters(self, work_dir: Optional[str] = None) -> list[str]:
        """Get list of available linter names."""
        workspace_tools = detect_tools(work_dir=work_dir)
        return [tool.name for tool in workspace_tools.linters if tool.available]

    def _get_available_formatters(self, work_dir: Optional[str] = None) -> list[str]:
        """Get list of available formatter names."""
        workspace_tools = detect_tools(work_dir=work_dir)
        return [tool.name for tool in workspace_tools.formatters if tool.available]

    def _get_available_testers(self, work_dir: Optional[str] = None) -> list[str]:
        """Get list of available tester names."""
        workspace_tools = detect_tools(work_dir=work_dir)
        return [tool.name for tool in workspace_tools.testers if tool.available]

    def _count_formatted_files(self, tool_name: str, output: str) -> int:
        """Count formatted files from tool output."""
        if not output:
            return 0

        if tool_name == "black":
            return output.lower().count("reformatted")
        elif tool_name == "ruff":
            lines = output.split("\n")
            return len(
                [
                    line
                    for line in lines
                    if line.strip()
                    and not line.startswith("Found")
                    and not line.startswith("Formatting")
                ]
            )
        elif tool_name == "isort":
            return output.lower().count("fixing") + output.lower().count("fixed")
        else:
            # For other formatters, assume all files were processed if successful
            return 1 if output else 0

    def _parse_test_output(self, tool_name: str, output: str) -> tuple[int, int, int]:
        """Parse test output to extract counts."""
        import re

        tests_run = 0
        tests_passed = 0
        tests_failed = 0

        if tool_name == "pytest":
            # Look for pytest summary
            passed_match = re.search(r"(\d+)\s+passed", output)
            if passed_match:
                tests_passed = int(passed_match.group(1))
                tests_run += tests_passed

            failed_match = re.search(r"(\d+)\s+failed", output)
            if failed_match:
                tests_failed = int(failed_match.group(1))
                tests_run += tests_failed

        elif tool_name in ["nose2", "unittest"]:
            # Look for "Ran X tests"
            ran_match = re.search(r"Ran\s+(\d+)\s+test[s]?", output)
            if ran_match:
                tests_run = int(ran_match.group(1))

            if "FAILED" in output:
                # Try to extract failure count
                fail_match = re.search(r"failures=(\d+)", output)
                error_match = re.search(r"errors=(\d+)", output)

                failures = int(fail_match.group(1)) if fail_match else 0
                errors = int(error_match.group(1)) if error_match else 0
                tests_failed = failures + errors

            tests_passed = tests_run - tests_failed

        return tests_run, tests_passed, tests_failed

    def _format_success(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format success result."""
        formatter = self._config_manager.get_formatter()
        return formatter.format_success(tool_name, message, details)

    def _format_warning(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format warning result."""
        formatter = self._config_manager.get_formatter()
        return formatter.format_warning(tool_name, message, details)

    def _format_error(
        self, tool_name: str, message: str, details: Optional[str] = None
    ) -> str:
        """Format error result."""
        formatter = self._config_manager.get_formatter()
        return formatter.format_error(tool_name, message, details)
