"""Basic tests for Python LFT components."""

import pytest

from python_lft.core.models import CommandResult, ToolConfig, WorkspaceTools
from python_lft.services.workspace import detect_tools, get_python_files


class TestBasicFunctionality:
    """Test basic functionality of core components."""

    def test_command_result_creation(self):
        """Test CommandResult model creation."""
        result = CommandResult(exit_code=0, stdout="Test output", stderr="")
        assert result.exit_code == 0
        assert result.stdout == "Test output"
        assert result.success is True

    def test_tool_config_creation(self):
        """Test ToolConfig model creation."""
        config = ToolConfig(
            name="ruff", command="ruff", available=True, config_files=["pyproject.toml"]
        )
        assert config.name == "ruff"
        assert config.command == "ruff"
        assert config.available is True
        assert config.config_files == ["pyproject.toml"]

    def test_workspace_tools_creation(self):
        """Test WorkspaceTools model creation."""
        tools = WorkspaceTools(linters=[], formatters=[], testers=[], config_files={})
        assert isinstance(tools.linters, list)
        assert isinstance(tools.formatters, list)
        assert isinstance(tools.testers, list)
        assert isinstance(tools.config_files, dict)

    def test_get_python_files_basic(self):
        """Test basic Python file detection."""
        # This should work even in an empty directory
        files = get_python_files("all")
        assert isinstance(files, list)

    def test_detect_tools_basic(self):
        """Test basic tool detection."""
        # This should work even without configured tools
        tools = detect_tools()
        assert isinstance(tools, WorkspaceTools)
        assert isinstance(tools.linters, list)
        assert isinstance(tools.formatters, list)
        assert isinstance(tools.testers, list)


class TestWorkspaceFunctions:
    """Test workspace detection functions."""

    def test_detect_tools_returns_workspace_tools(self):
        """Test that detect_tools returns WorkspaceTools instance."""
        result = detect_tools()
        assert isinstance(result, WorkspaceTools)

    def test_get_python_files_returns_list(self):
        """Test that get_python_files returns list."""
        result = get_python_files()
        assert isinstance(result, list)

    def test_get_python_files_with_target(self):
        """Test get_python_files with specific target."""
        result = get_python_files("nonexistent.py")
        assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__])
