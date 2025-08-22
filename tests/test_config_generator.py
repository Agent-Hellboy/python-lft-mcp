"""Tests for config_generator module."""

import json
from unittest.mock import patch

from python_lft.config_generator import generate_mcp_config, main, print_config


class TestConfigGenerator:
    """Test config generator functionality."""

    def test_generate_mcp_config(self):
        """Test MCP configuration generation."""
        config = generate_mcp_config()

        # Verify structure
        assert "mcpServers" in config
        assert "python-lft" in config["mcpServers"]

        server_config = config["mcpServers"]["python-lft"]
        assert "command" in server_config
        assert "description" in server_config
        assert "args" in server_config

        # Verify content
        assert server_config["command"] == "python"
        assert "Python Lint, Format, Test" in server_config["description"]
        assert server_config["args"] == ["-m", "python_lft"]

    def test_generate_mcp_config_structure(self):
        """Test the detailed structure of generated config."""
        config = generate_mcp_config()

        # Check that all expected keys are present
        server_config = config["mcpServers"]["python-lft"]
        expected_keys = ["command", "description", "args"]

        for key in expected_keys:
            assert key in server_config

    def test_generate_mcp_config_json_serializable(self):
        """Test that generated config is JSON serializable."""
        config = generate_mcp_config()

        # Should not raise an exception
        json_str = json.dumps(config, indent=2)
        assert isinstance(json_str, str)
        assert len(json_str) > 0

    @patch("builtins.print")
    def test_print_config(self, mock_print):
        """Test configuration printing."""
        print_config()

        # Verify print was called
        mock_print.assert_called()

        # Get the printed content (handle empty calls)
        call_args = []
        for call in mock_print.call_args_list:
            if call.args:
                call_args.append(call.args[0])
            else:
                call_args.append("")  # Empty print() calls
        printed_content = "\n".join(call_args)

        # Verify content contains expected elements
        assert "MCP Configuration for Python LFT" in printed_content
        assert "python" in printed_content  # Command should be python
        assert "Copy the following configuration" in printed_content

    @patch("builtins.print")
    def test_print_config_instructions(self, mock_print):
        """Test that print_config includes usage instructions."""
        print_config()

        # Get all printed content (handle empty calls)
        call_args = []
        for call in mock_print.call_args_list:
            if call.args:
                call_args.append(call.args[0])
            else:
                call_args.append("")
        printed_content = "\n".join(call_args)

        # Check for instructions
        assert "MCP Configuration for Python LFT" in printed_content
        assert "Copy the following configuration" in printed_content
        assert "mcpServers" in printed_content

    @patch("builtins.print")
    def test_print_config_json_format(self, mock_print):
        """Test that printed config is valid JSON format."""
        print_config()

        # Find the JSON part in the printed output (handle empty calls)
        call_args = []
        for call in mock_print.call_args_list:
            if call.args:
                call_args.append(call.args[0])
            else:
                call_args.append("")

        # Look for the JSON content (lines that start with { or contain JSON)
        json_lines = []
        capture_json = False

        for line in call_args:
            if line.strip().startswith("{"):
                capture_json = True
            if capture_json:
                json_lines.append(line)
            if line.strip().endswith("}") and capture_json:
                break

        if json_lines:
            json_content = "\n".join(json_lines)
            # Should be valid JSON
            parsed = json.loads(json_content)
            assert "mcpServers" in parsed

    @patch("python_lft.config_generator.print_usage_instructions")
    def test_main_function(self, mock_print_usage):
        """Test the main function."""
        main()

        # Verify print_usage_instructions was called (that's what main actually calls)
        mock_print_usage.assert_called_once()

    def test_config_values(self):
        """Test specific configuration values."""
        config = generate_mcp_config()
        server_config = config["mcpServers"]["python-lft"]

        # Test specific values
        assert server_config["command"] == "python"
        assert isinstance(server_config["args"], list)
        assert server_config["args"] == ["-m", "python_lft"]
        assert "Python Lint, Format, Test" in server_config["description"]

    def test_config_reproducibility(self):
        """Test that config generation is reproducible."""
        config1 = generate_mcp_config()
        config2 = generate_mcp_config()

        # Should generate identical configs
        assert config1 == config2

    @patch("builtins.print")
    def test_print_config_header_footer(self, mock_print):
        """Test that print_config includes proper header and footer."""
        print_config()

        call_args = []
        for call in mock_print.call_args_list:
            if call.args:
                call_args.append(call.args[0])
            else:
                call_args.append("")
        printed_content = call_args

        # Check for header
        assert any(
            "MCP Configuration for Python LFT" in line for line in printed_content
        )

        # Check for instructions
        assert any(
            "Copy the following configuration" in line for line in printed_content
        )

    def test_config_schema_compliance(self):
        """Test that generated config follows expected MCP schema."""
        config = generate_mcp_config()

        # Should have top-level mcpServers
        assert "mcpServers" in config
        assert isinstance(config["mcpServers"], dict)

        # Should have python-lft server
        assert "python-lft" in config["mcpServers"]
        server = config["mcpServers"]["python-lft"]

        # Required fields
        assert "command" in server
        assert "description" in server
        assert "args" in server

        # Correct types
        assert isinstance(server["command"], str)
        assert isinstance(server["description"], str)
        assert isinstance(server["args"], list)

    @patch("python_lft.config_generator.json.dumps")
    @patch("builtins.print")
    def test_print_config_json_formatting(self, mock_print, mock_json_dumps):
        """Test that JSON is formatted correctly in print_config."""
        mock_json_dumps.return_value = '{"test": "json"}'

        print_config()

        # Verify json.dumps was called with proper formatting
        mock_json_dumps.assert_called()
        call_kwargs = mock_json_dumps.call_args.kwargs
        assert call_kwargs.get("indent") == 2
        assert call_kwargs.get("sort_keys") is True

    def test_args_list_content(self):
        """Test that args list contains expected module reference."""
        config = generate_mcp_config()
        server_config = config["mcpServers"]["python-lft"]

        assert server_config["args"] == ["-m", "python_lft"]
        assert len(server_config["args"]) == 2

    def test_description_content(self):
        """Test description contains key information."""
        config = generate_mcp_config()
        description = config["mcpServers"]["python-lft"]["description"]

        # Should mention key features
        assert "Python" in description
        assert any(word in description.lower() for word in ["lint", "format", "test"])

    @patch("sys.argv", ["python-lft-config"])
    @patch("python_lft.config_generator.print_usage_instructions")
    def test_main_as_script(self, mock_print_usage):
        """Test main function when called as script."""
        main()
        mock_print_usage.assert_called_once()
