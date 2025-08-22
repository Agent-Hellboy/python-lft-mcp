"""Tests for python_lft.tools_api module."""

from unittest.mock import MagicMock, patch

import pytest

from python_lft.core.models import ToolConfig, WorkspaceTools


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
    @pytest.mark.asyncio
    async def test_lint_function(self, mock_orchestrator_class):
        """Test lint function."""
        from python_lft.tools_api import lint

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock the async lint method
        async def mock_lint(*args, **kwargs):
            return "Clean lint result"

        mock_orchestrator.lint = mock_lint

        result = await lint(target="test.py")

        # Verify result structure
        assert result["exit_code"] == 0
        assert result["success"] is True

    @patch("python_lft.tools_api.ToolOrchestrator")
    @pytest.mark.asyncio
    async def test_format_code_function(self, mock_orchestrator_class):
        """Test format_code function."""
        from python_lft.tools_api import format_code

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock the async format method
        async def mock_format(*args, **kwargs):
            return "Format result"

        mock_orchestrator.format = mock_format

        result = await format_code(target="test.py")

        # Verify result structure
        assert result["exit_code"] == 0
        assert result["success"] is True

    @patch("python_lft.tools_api.ToolOrchestrator")
    @pytest.mark.asyncio
    async def test_test_function(self, mock_orchestrator_class):
        """Test test function."""
        from python_lft.tools_api import test

        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock the async test method
        async def mock_test(*args, **kwargs):
            return "Test result"

        mock_orchestrator.test = mock_test

        result = await test(target="tests/")

        # Verify result structure
        assert result["exit_code"] == 0
        assert result["success"] is True

    def test_tools_api_imports(self):
        """Test that tools API can be imported."""
        from python_lft.tools_api import detect_workspace_tools, format_code, lint, test

        assert callable(detect_workspace_tools)
        assert callable(lint)
        assert callable(format_code)
        assert callable(test)
