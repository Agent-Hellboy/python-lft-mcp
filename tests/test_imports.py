"""Test that all main modules can be imported."""

import pytest


class TestImports:
    """Test that all main modules can be imported without errors."""

    def test_import_core_models(self):
        """Test importing core models."""
        from python_lft.core.models import CommandResult, ToolConfig, WorkspaceTools

        assert CommandResult is not None
        assert ToolConfig is not None
        assert WorkspaceTools is not None

    def test_import_workspace_services(self):
        """Test importing workspace services."""
        from python_lft.services.workspace import detect_tools, get_python_files

        assert detect_tools is not None
        assert get_python_files is not None

    def test_import_orchestrator(self):
        """Test importing orchestrator."""
        from python_lft.services.orchestrator import ToolOrchestrator

        assert ToolOrchestrator is not None

    def test_import_factories(self):
        """Test importing executor factories."""
        from python_lft.executors.factories import (
            FormatterFactory,
            LinterFactory,
            TesterFactory,
        )

        assert LinterFactory is not None
        assert FormatterFactory is not None
        assert TesterFactory is not None

    def test_import_main_api(self):
        """Test importing main API."""
        from python_lft import create_mcp, detect_tools, get_python_files

        assert create_mcp is not None
        assert detect_tools is not None
        assert get_python_files is not None

    def test_import_tools_api(self):
        """Test importing tools API."""
        from python_lft.tools_api import register_tools

        assert register_tools is not None


if __name__ == "__main__":
    pytest.main([__file__])
