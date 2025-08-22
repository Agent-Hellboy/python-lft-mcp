"""Tests for python_lft.cli module."""

from unittest.mock import MagicMock, patch

import pytest


class TestCLI:
    """Test CLI module functionality."""

    @patch("python_lft.cli.logging.basicConfig")
    @patch("python_lft.app.create_mcp")
    def test_main_function(self, mock_create_mcp, mock_logging):
        """Test main function execution."""
        from python_lft.cli import main

        mock_mcp = MagicMock()
        mock_create_mcp.return_value = mock_mcp
        mock_mcp.run.side_effect = KeyboardInterrupt()  # Simulate graceful shutdown

        try:
            main()
        except KeyboardInterrupt:
            pass  # Expected from our mock

        # Should setup logging
        mock_logging.assert_called_once()

        # Should create MCP
        mock_create_mcp.assert_called_once()

        # Should attempt to run
        mock_mcp.run.assert_called_once()

    def test_cli_imports(self):
        """Test that CLI module can be imported."""
        from python_lft.cli import main

        assert callable(main)
