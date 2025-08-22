"""Tests for python_lft.core.models module."""

from python_lft.core.models import CommandResult, ToolConfig, WorkspaceTools


class TestCoreModels:
    """Test core models functionality."""

    def test_command_result(self):
        """Test CommandResult model."""
        # Test successful result
        result = CommandResult(exit_code=0, stdout="output", stderr="")
        assert result.exit_code == 0
        assert result.stdout == "output"
        assert result.stderr == ""
        assert result.success is True

        # Test failed result
        result_fail = CommandResult(exit_code=1, stdout="", stderr="error")
        assert result_fail.exit_code == 1
        assert result_fail.success is False

    def test_tool_config(self):
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

    def test_workspace_tools(self):
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

    def test_workspace_tools_empty(self):
        """Test WorkspaceTools with no tools."""
        tools = WorkspaceTools(linters=[], formatters=[], testers=[], config_files={})

        assert tools.get_best_linter() is None
        assert tools.get_best_formatter() is None
        assert tools.get_best_tester() is None
