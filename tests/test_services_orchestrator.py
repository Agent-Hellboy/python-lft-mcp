"""Tests for python_lft.services.orchestrator module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from python_lft.core.models import CommandResult, ToolConfig, WorkspaceTools
from python_lft.services.orchestrator import ToolOrchestrator


class TestOrchestrator:
    """Test orchestrator module functionality."""

    def test_orchestrator_creation(self):
        """Test that ToolOrchestrator can be created."""
        orchestrator = ToolOrchestrator()
        assert orchestrator is not None
        assert hasattr(orchestrator, "lint")
        assert hasattr(orchestrator, "format")
        assert hasattr(orchestrator, "test")

    @patch("python_lft.services.orchestrator.get_python_files")
    @patch("python_lft.services.orchestrator.detect_tools")
    @pytest.mark.asyncio
    async def test_lint_no_files(self, mock_detect, mock_get_files):
        """Test linting with no files found."""
        mock_get_files.return_value = []
        mock_detect.return_value = WorkspaceTools(
            linters=[], formatters=[], testers=[], config_files={}
        )

        orchestrator = ToolOrchestrator()
        result = await orchestrator.lint()

        assert isinstance(result, str)
        assert "No Python files found" in result

    @patch("python_lft.services.orchestrator.get_python_files")
    @patch("python_lft.services.orchestrator.detect_tools")
    @pytest.mark.asyncio
    async def test_lint_no_tools(self, mock_detect, mock_get_files):
        """Test linting with no tools available."""
        mock_get_files.return_value = ["test.py"]
        mock_detect.return_value = WorkspaceTools(
            linters=[], formatters=[], testers=[], config_files={}
        )

        orchestrator = ToolOrchestrator()
        result = await orchestrator.lint()

        assert isinstance(result, str)
        assert "No linter available" in result

    @patch("python_lft.services.orchestrator.get_python_files")
    @patch("python_lft.services.orchestrator.detect_tools")
    @pytest.mark.asyncio
    async def test_format_no_tools(self, mock_detect, mock_get_files):
        """Test formatting with no tools available."""
        mock_get_files.return_value = ["test.py"]
        mock_detect.return_value = WorkspaceTools(
            linters=[], formatters=[], testers=[], config_files={}
        )

        orchestrator = ToolOrchestrator()
        result = await orchestrator.format()

        assert isinstance(result, str)
        assert "No formatter available" in result

    @patch("python_lft.services.orchestrator.get_python_files")
    @patch("python_lft.services.orchestrator.detect_tools")
    @pytest.mark.asyncio
    async def test_test_no_tools(self, mock_detect, mock_get_files):
        """Test testing with no tools available."""
        mock_get_files.return_value = ["test.py"]
        mock_detect.return_value = WorkspaceTools(
            linters=[], formatters=[], testers=[], config_files={}
        )

        orchestrator = ToolOrchestrator()
        result = await orchestrator.test()

        assert isinstance(result, str)
        assert "No test runner available" in result
