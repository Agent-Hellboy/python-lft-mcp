"""Tests for python_lft.app module."""

from unittest.mock import MagicMock, patch


class TestApp:
    """Test app module functionality."""

    @patch("python_lft.app.register_tools")
    @patch("python_lft.app.FastMCP")
    def test_create_mcp(self, mock_fastmcp, mock_register):
        """Test create_mcp function."""
        from python_lft.app import create_mcp

        mock_mcp = MagicMock()
        mock_fastmcp.return_value = mock_mcp

        result = create_mcp()

        # Should create FastMCP instance
        mock_fastmcp.assert_called_once()
        call_kwargs = mock_fastmcp.call_args.kwargs
        assert call_kwargs["name"] == "python-lft"
        assert "dependencies" in call_kwargs

        # Should register tools
        mock_register.assert_called_once_with(mock_mcp)

        # Should return the MCP instance
        assert result == mock_mcp

    def test_app_imports(self):
        """Test that app module can be imported."""
        from python_lft.app import create_mcp

        assert callable(create_mcp)
