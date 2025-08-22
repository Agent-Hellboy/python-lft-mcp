"""MCP tool API layer - thin wrappers calling service functions."""

import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .services.orchestrator import ToolOrchestrator
from .services.workspace import detect_tools


logger = logging.getLogger(__name__)


def detect_workspace_tools(work_dir: str = ".") -> dict:
    """
    Analyze a Python project's configuration files to discover which development tools are configured.

    Args:
        work_dir: Directory to analyze (defaults to current directory)

    Returns:
        Dictionary containing discovered tools and their configurations
    """
    try:
        orchestrator = ToolOrchestrator()
        tools = detect_tools(work_dir=work_dir)

        return {
            "linters": [
                {
                    "name": tool.name,
                    "command": tool.command,
                    "available": tool.available,
                    "config_files": tool.config_files,
                    "config_data": tool.config_data,
                }
                for tool in tools.linters
            ],
            "formatters": [
                {
                    "name": tool.name,
                    "command": tool.command,
                    "available": tool.available,
                    "config_files": tool.config_files,
                    "config_data": tool.config_data,
                }
                for tool in tools.formatters
            ],
            "testers": [
                {
                    "name": tool.name,
                    "command": tool.command,
                    "available": tool.available,
                    "config_files": tool.config_files,
                    "config_data": tool.config_data,
                }
                for tool in tools.testers
            ],
            "config_files": tools.config_files,
        }
    except Exception as e:
        logger.error(f"Error detecting workspace tools: {e}")
        return {"linters": [], "formatters": [], "testers": [], "config_files": {}}


def lint(
    target: str = "all",
    exact_tool: str = "auto",
    tool_config: Optional[dict] = None,
    custom_args: Optional[list] = None,
    work_dir: str = ".",
) -> dict:
    """
    Automatically format Python code to improve readability and enforce consistent style.

    Args:
        target: Files or directories to lint ("all" for entire project)
        exact_tool: Specific linter tool to use ("auto" for best available)
        tool_config: Custom configuration for the tool
        custom_args: Additional command-line arguments
        work_dir: Working directory to run the command in

    Returns:
        Dictionary with execution results
    """
    try:
        orchestrator = ToolOrchestrator()
        result = orchestrator.lint(
            target=target,
            exact_tool=exact_tool,
            tool_config=tool_config,
            custom_args=custom_args,
            work_dir=work_dir,
        )

        return {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.success,
        }
    except Exception as e:
        logger.error(f"Error running linter: {e}")
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": str(e),
            "success": False,
        }


def format_code(
    target: str = "all",
    exact_tool: str = "auto",
    tool_config: Optional[dict] = None,
    custom_args: Optional[list] = None,
    work_dir: str = ".",
) -> dict:
    """
    Automatically format Python code to improve readability and enforce consistent style.

    Args:
        target: Files or directories to format ("all" for entire project)
        exact_tool: Specific formatter tool to use ("auto" for best available)
        tool_config: Custom configuration for the tool
        custom_args: Additional command-line arguments
        work_dir: Working directory to run the command in

    Returns:
        Dictionary with execution results
    """
    try:
        orchestrator = ToolOrchestrator()
        result = orchestrator.format(
            target=target,
            exact_tool=exact_tool,
            tool_config=tool_config,
            custom_args=custom_args,
            work_dir=work_dir,
        )

        return {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.success,
        }
    except Exception as e:
        logger.error(f"Error running formatter: {e}")
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": str(e),
            "success": False,
        }


def test(
    target: str = "all",
    exact_tool: str = "auto",
    tool_config: Optional[dict] = None,
    custom_args: Optional[list] = None,
    work_dir: str = ".",
) -> dict:
    """
    Execute test suites to verify code functionality and catch regressions.

    Args:
        target: Files or directories to test ("all" for entire project)
        exact_tool: Specific test tool to use ("auto" for best available)
        tool_config: Custom configuration for the tool
        custom_args: Additional command-line arguments
        work_dir: Working directory to run the command in

    Returns:
        Dictionary with execution results
    """
    try:
        orchestrator = ToolOrchestrator()
        result = orchestrator.test(
            target=target,
            exact_tool=exact_tool,
            tool_config=tool_config,
            custom_args=custom_args,
            work_dir=work_dir,
        )

        return {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.success,
        }
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": str(e),
            "success": False,
        }


def register_tools(mcp: FastMCP) -> None:
    """Register all MCP tools with the FastMCP instance."""

    # Create orchestrator instance
    orchestrator = ToolOrchestrator()

    @mcp.tool(
        name="detect_workspace_tools",
        description="Analyze Python project configuration to discover which linting, formatting, and testing tools are configured",
    )
    async def detect_workspace_tools(work_dir: str = ".") -> dict:
        """
        Analyze a Python project's configuration files (pyproject.toml, setup.cfg, tox.ini, etc.)
        to discover which development tools are configured.

        **When to use this tool:**
        - Before running any linting, formatting, or testing operations
        - To understand what tools a Python project has configured
        - To see which config files exist in a project
        - As a first step when analyzing any Python codebase

        **What this tool returns:**
        - Lists of configured linters (ruff, flake8, pylint, mypy, etc.) with their config files
        - Lists of configured formatters (black, ruff, isort, etc.) with their config files
        - Lists of configured test runners (pytest, nose2, unittest) with their config files
        - Map of all config files found (pyproject.toml, tox.ini, etc.)
        - Recommendations for best tools to use based on project configuration

        Args:
            work_dir: Target directory to analyze (default: current directory)

        Returns:
            Dictionary with 'linters', 'formatters', 'testers', 'config_files', and 'recommended' keys
        """
        logger.info(f"MCP detect_workspace_tools tool called for directory: {work_dir}")
        workspace_tools = detect_tools(work_dir=work_dir if work_dir != "." else None)

        return {
            "linters": [
                {
                    "name": tool.name,
                    "command": tool.command,
                    "available": tool.available,
                    "config_files": tool.config_files,
                }
                for tool in workspace_tools.linters
            ],
            "formatters": [
                {
                    "name": tool.name,
                    "command": tool.command,
                    "available": tool.available,
                    "config_files": tool.config_files,
                }
                for tool in workspace_tools.formatters
            ],
            "testers": [
                {
                    "name": tool.name,
                    "command": tool.command,
                    "available": tool.available,
                    "config_files": tool.config_files,
                }
                for tool in workspace_tools.testers
            ],
            "config_files": workspace_tools.config_files,
            "recommended": {
                "linter": (
                    workspace_tools.get_best_linter().name
                    if workspace_tools.get_best_linter()
                    else None
                ),
                "formatter": (
                    workspace_tools.get_best_formatter().name
                    if workspace_tools.get_best_formatter()
                    else None
                ),
                "tester": (
                    workspace_tools.get_best_tester().name
                    if workspace_tools.get_best_tester()
                    else None
                ),
            },
        }

    @mcp.tool(
        name="lint",
        description="Execute specific linting tools with custom configuration on Python code",
    )
    async def lint(
        target: str = "all",
        exact_tool: str = "auto",
        tool_config: Optional[dict] = None,
        custom_args: Optional[list] = None,
        work_dir: str = ".",
    ) -> str:
        """
        Execute linting tools with precise configuration control.

        **When to use this tool:**
        - After running detect_workspace_tools to understand project configuration
        - To run specific linters with exact settings found in project configs
        - To check code quality with project-specific rules and parameters

        **How to use this tool:**
        1. First call detect_workspace_tools to get available linters and their configurations
        2. Use the specific tool name and configuration from the detection results
        3. Pass any custom arguments needed for the specific use case

        **Examples:**
        - lint(exact_tool="ruff", tool_config={"line-length": 88, "target-version": "py39"})
        - lint(exact_tool="mypy", custom_args=["--strict", "--no-error-summary"])
        - lint(exact_tool="flake8", tool_config={"max-line-length": "120"})

        Args:
            target: Target to lint - "all" for entire project, or specific file path (default: "all")
            exact_tool: Specific linter to execute (ruff, flake8, pylint, mypy, bandit) or "auto" (default: "auto")
            tool_config: Configuration dictionary with tool-specific settings (default: None)
            custom_args: List of additional command-line arguments for the tool (default: None)
            work_dir: Target project directory to analyze (default: current directory)

        Returns:
            Detailed linting results with specific tool output and configuration used
        """
        logger.info(
            f"MCP lint tool called with target: {target}, exact_tool: {exact_tool}, tool_config: {tool_config}, work_dir: {work_dir}"
        )
        return await orchestrator.lint_with_config(
            target=target,
            exact_tool=exact_tool if exact_tool != "auto" else None,
            tool_config=tool_config or {},
            custom_args=custom_args or [],
            work_dir=work_dir if work_dir != "." else None,
        )

    @mcp.tool(
        name="format",
        description="Execute specific formatting tools with custom configuration on Python code",
    )
    async def format_code(
        target: str = "all",
        exact_tool: str = "auto",
        tool_config: Optional[dict] = None,
        custom_args: Optional[list] = None,
        work_dir: str = ".",
    ) -> str:
        """
        Execute formatting tools with precise configuration control.

        **When to use this tool:**
        - After running detect_workspace_tools to understand project formatting setup
        - To run specific formatters with exact settings found in project configs
        - To apply consistent code formatting with project-specific rules

        **How to use this tool:**
        1. First call detect_workspace_tools to get available formatters and their configurations
        2. Use the specific tool name and configuration from the detection results
        3. Pass any custom arguments needed for the specific formatting requirements

        **Examples:**
        - format_code(exact_tool="black", tool_config={"line-length": 88, "target-version": ["py39"]})
        - format_code(exact_tool="ruff", tool_config={"line-length": 120}, custom_args=["--fix"])
        - format_code(exact_tool="isort", tool_config={"profile": "black", "line_length": 88})

        Args:
            target: Target to format - "all" for entire project, or specific file path (default: "all")
            exact_tool: Specific formatter to execute (black, ruff, isort, autopep8, yapf) or "auto" (default: "auto")
            tool_config: Configuration dictionary with tool-specific settings (default: None)
            custom_args: List of additional command-line arguments for the tool (default: None)
            work_dir: Target project directory to format (default: current directory)

        Returns:
            Formatting results showing which files were changed and tool configuration used
        """
        logger.info(
            f"MCP format tool called with target: {target}, exact_tool: {exact_tool}, tool_config: {tool_config}, work_dir: {work_dir}"
        )
        return await orchestrator.format_with_config(
            target=target,
            exact_tool=exact_tool if exact_tool != "auto" else None,
            tool_config=tool_config or {},
            custom_args=custom_args or [],
            work_dir=work_dir if work_dir != "." else None,
        )

    @mcp.tool(
        name="test",
        description="Execute specific test runners with custom configuration to verify code functionality",
    )
    async def test(
        target: str = "all",
        exact_tool: str = "auto",
        tool_config: Optional[dict] = None,
        custom_args: Optional[list] = None,
        work_dir: str = ".",
    ) -> str:
        """
        Execute test runners with precise configuration control.

        **When to use this tool:**
        - After running detect_workspace_tools to understand project testing setup
        - To run specific test frameworks with exact settings found in project configs
        - To execute tests with project-specific parameters and configurations

        **How to use this tool:**
        1. First call detect_workspace_tools to get available test runners and their configurations
        2. Use the specific tool name and configuration from the detection results
        3. Pass any custom arguments needed for specific testing requirements

        **Examples:**
        - test(exact_tool="pytest", tool_config={"testpaths": ["tests"], "addopts": "-v --tb=short"})
        - test(exact_tool="pytest", custom_args=["-k", "test_integration", "--cov=src"])
        - test(exact_tool="unittest", tool_config={"start_directory": "tests"})

        Args:
            target: Target to test - "all" for entire test suite, or specific test file/directory (default: "all")
            exact_tool: Specific test runner to execute (pytest, nose2, unittest) or "auto" (default: "auto")
            tool_config: Configuration dictionary with test-specific settings (default: None)
            custom_args: List of additional command-line arguments for the test runner (default: None)
            work_dir: Target project directory containing tests (default: current directory)

        Returns:
            Test execution results with specific runner output and configuration used
        """
        logger.info(
            f"MCP test tool called with target: {target}, exact_tool: {exact_tool}, tool_config: {tool_config}, work_dir: {work_dir}"
        )
        return await orchestrator.test_with_config(
            target=target,
            exact_tool=exact_tool if exact_tool != "auto" else None,
            tool_config=tool_config or {},
            custom_args=custom_args or [],
            work_dir=work_dir if work_dir != "." else None,
        )

    @mcp.tool(name="check_config_files", description="Check for common config files")
    async def check_config_files() -> dict:
        """
        Check for common Python configuration files in the workspace.

        Returns:
            Dictionary mapping config file names to boolean indicating if they exist
        """
        logger.info("MCP check_config_files tool called")
        workspace_tools = detect_tools()
        return workspace_tools.config_files
