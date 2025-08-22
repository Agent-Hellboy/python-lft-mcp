"""Core functionality tests for python_lft package."""

from unittest.mock import MagicMock, patch

import pytest

from python_lft.core.models import CommandResult, ToolConfig, WorkspaceTools


class TestPythonLftCore:
    """Test core python_lft functionality."""

    def test_command_result_creation(self):
        """Test CommandResult model."""
        result = CommandResult(exit_code=0, stdout="output", stderr="")
        assert result.exit_code == 0
        assert result.stdout == "output"
        assert result.stderr == ""
        assert result.success is True

        result_error = CommandResult(exit_code=1, stdout="", stderr="error")
        assert result_error.success is False

    def test_tool_config_creation(self):
        """Test ToolConfig model."""
        config = ToolConfig(
            name="ruff",
            command="ruff",
            available=True,
            config_files=["pyproject.toml"],
            config_data={"line-length": 88},
        )
        assert config.name == "ruff"
        assert config.command == "ruff"
        assert config.available is True
        assert config.config_files == ["pyproject.toml"]
        assert config.config_data == {"line-length": 88}

    def test_workspace_tools_creation(self):
        """Test WorkspaceTools model."""
        linter = ToolConfig(
            name="ruff", command="ruff", available=True, config_files=[], config_data={}
        )
        formatter = ToolConfig(
            name="black",
            command="black",
            available=True,
            config_files=[],
            config_data={},
        )
        tester = ToolConfig(
            name="pytest",
            command="pytest",
            available=True,
            config_files=[],
            config_data={},
        )

        tools = WorkspaceTools(
            linters=[linter],
            formatters=[formatter],
            testers=[tester],
            config_files={"pyproject.toml": True},
        )

        assert len(tools.linters) == 1
        assert len(tools.formatters) == 1
        assert len(tools.testers) == 1
        assert tools.config_files == {"pyproject.toml": True}

        # Test best tool selection
        assert tools.get_best_linter() == linter
        assert tools.get_best_formatter() == formatter
        assert tools.get_best_tester() == tester

    @patch("python_lft.tools_api.detect_tools")
    def test_detect_workspace_tools(self, mock_detect):
        """Test workspace detection functionality."""
        from python_lft.tools_api import detect_workspace_tools

        mock_detect.return_value = WorkspaceTools(
            linters=[
                ToolConfig(
                    name="ruff",
                    command="ruff",
                    available=True,
                    config_files=[],
                    config_data={},
                )
            ],
            formatters=[],
            testers=[],
            config_files={},
        )

        result = detect_workspace_tools()

        assert "linters" in result
        assert "formatters" in result
        assert "testers" in result
        assert "config_files" in result
        assert len(result["linters"]) == 1
        assert result["linters"][0]["name"] == "ruff"

    @patch("python_lft.tools_api.ToolOrchestrator")
    @pytest.mark.asyncio
    async def test_lint_function(self, mock_orchestrator_class):
        """Test lint function flow."""
        from python_lft.tools_api import lint

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock the async lint method
        async def mock_lint(*args, **kwargs):
            return "Clean lint result"

        mock_orchestrator.lint = mock_lint

        result = await lint(target="test.py")

        assert result["exit_code"] == 0
        assert result["success"] is True

    @patch("python_lft.tools_api.ToolOrchestrator")
    @pytest.mark.asyncio
    async def test_format_function(self, mock_orchestrator_class):
        """Test format function flow."""
        from python_lft.tools_api import format_code

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock the async format method
        async def mock_format(*args, **kwargs):
            return "Format result"

        mock_orchestrator.format = mock_format

        result = await format_code(target="test.py")

        assert result["exit_code"] == 0
        assert result["success"] is True

    @patch("python_lft.tools_api.ToolOrchestrator")
    @pytest.mark.asyncio
    async def test_test_function(self, mock_orchestrator_class):
        """Test test function flow."""
        from python_lft.tools_api import test

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock the async test method
        async def mock_test(*args, **kwargs):
            return "Test result"

        mock_orchestrator.test = mock_test

        result = await test(target="tests/")

        assert result["exit_code"] == 0
        assert result["success"] is True

    def test_config_generator(self):
        """Test MCP config generation."""
        from python_lft.config_generator import generate_mcp_config

        config = generate_mcp_config()

        assert "mcpServers" in config
        assert "python-lft" in config["mcpServers"]
        server_config = config["mcpServers"]["python-lft"]
        assert server_config["command"] == "python"
        assert server_config["args"] == ["-m", "python_lft"]

    def test_app_create_mcp(self):
        """Test MCP app creation."""
        with (
            patch("python_lft.app.FastMCP") as mock_fastmcp,
            patch("python_lft.app.register_tools") as mock_register,
        ):
            from python_lft.app import create_mcp

            mock_mcp = MagicMock()
            mock_fastmcp.return_value = mock_mcp

            result = create_mcp()

            mock_fastmcp.assert_called_once()
            mock_register.assert_called_once_with(mock_mcp)
            assert result == mock_mcp

    def test_main_module_exists(self):
        """Test that main module can be imported."""
        from python_lft import __main__

        assert hasattr(__main__, "main")
        assert callable(__main__.main)

    def test_import_structure(self):
        """Test that core imports work."""
        # Test that we can import key components
        from python_lft.app import create_mcp
        from python_lft.config_generator import generate_mcp_config
        from python_lft.tools_api import detect_workspace_tools, format_code, lint, test

        # All should be callable/instantiable
        assert callable(detect_workspace_tools)
        assert callable(lint)
        assert callable(format_code)
        assert callable(test)
        assert callable(generate_mcp_config)
        assert callable(create_mcp)
