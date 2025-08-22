"""Tests for python_lft.tools_api module."""

from unittest.mock import MagicMock, patch

import pytest

from python_lft.core.models import CommandResult, ToolConfig, WorkspaceTools


class TestToolsAPI:
    """Test tools API module functionality."""

    @patch("python_lft.services.workspace.detect_tools")
    def test_detect_workspace_tools(self, mock_detect):
        """Test detect_workspace_tools function."""
        from python_lft.tools_api import detect_workspace_tools

        mock_tools = WorkspaceTools(
            linters=[
                ToolConfig(
                    name="ruff",
                    command="ruff",
                    available=True,
                    config_files=[],
                    config_data={},
                )
            ],
            formatters=[
                ToolConfig(
                    name="black",
                    command="black",
                    available=True,
                    config_files=[],
                    config_data={},
                )
            ],
            testers=[
                ToolConfig(
                    name="pytest",
                    command="pytest",
                    available=True,
                    config_files=[],
                    config_data={},
                )
            ],
            config_files={"pyproject.toml": True},
        )
        mock_detect.return_value = mock_tools

        result = detect_workspace_tools()

        # Verify structure
        assert "linters" in result
        assert "formatters" in result
        assert "testers" in result
        assert "config_files" in result

        # Verify content - the actual results may have more tools detected
        assert len(result["linters"]) >= 1
        assert any(linter["name"] == "ruff" for linter in result["linters"])
        assert len(result["formatters"]) >= 1
        assert any(formatter["name"] == "black" for formatter in result["formatters"])
        assert len(result["testers"]) >= 1
        assert any(tester["name"] == "pytest" for tester in result["testers"])

    @patch("python_lft.tools_api.ToolOrchestrator")
    def test_lint_function(self, mock_orchestrator_class):
        """Test lint function."""
        from python_lft.tools_api import lint

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_orchestrator.lint.return_value = CommandResult(
            exit_code=0, stdout="Clean", stderr=""
        )

        result = lint(target="test.py")

        # Verify the function was called
        mock_orchestrator.lint.assert_called_once()

        # Verify result structure
        assert result["exit_code"] == 0
        assert result["success"] is True
        assert result["stdout"] == "Clean"

    @patch("python_lft.tools_api.ToolOrchestrator")
    def test_format_code_function(self, mock_orchestrator_class):
        """Test format_code function."""
        from python_lft.tools_api import format_code

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_orchestrator.format.return_value = CommandResult(
            exit_code=0, stdout="Formatted", stderr=""
        )

        result = format_code(target="test.py")

        # Verify the function was called
        mock_orchestrator.format.assert_called_once()

        # Verify result structure
        assert result["exit_code"] == 0
        assert result["success"] is True
        assert result["stdout"] == "Formatted"

    @patch("python_lft.tools_api.ToolOrchestrator")
    def test_test_function(self, mock_orchestrator_class):
        """Test test function."""
        from python_lft.tools_api import test

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_orchestrator.test.return_value = CommandResult(
            exit_code=0, stdout="Passed", stderr=""
        )

        result = test(target="tests/")

        # Verify the function was called
        mock_orchestrator.test.assert_called_once()

        # Verify result structure
        assert result["exit_code"] == 0
        assert result["success"] is True
        assert result["stdout"] == "Passed"

    def test_tools_api_imports(self):
        """Test that tools API can be imported."""
        from python_lft.tools_api import detect_workspace_tools, lint, format_code, test

        assert callable(detect_workspace_tools)
        assert callable(lint)
        assert callable(format_code)
        assert callable(test)
