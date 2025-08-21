#!/usr/bin/env python3
"""
Configuration generator for Python LFT MCP Server.
Generates MCP client configuration for users.
"""

import json


def generate_mcp_config():
    """Generate MCP configuration for the Python LFT server."""
    config = {
        "mcpServers": {
            "python-lft": {
                "command": "python",
                "args": ["-m", "python_lft"],
                "description": "Python Lint, Format, Test (LFT) - Intelligent Python development tools",
                "version": "1.0.0",
            }
        }
    }
    return config


def print_usage_instructions():
    """Print instructions for configuring MCP clients."""
    print("🔧 Python LFT MCP Server Configuration")
    print("=" * 50)
    print()
    print("✅ Package installed successfully!")
    print()
    print("📋 Next Steps:")
    print("1. Copy the configuration below to your MCP client")
    print("2. Restart your MCP client")
    print("3. Start using Python LFT tools!")
    print()
    print("📁 Common MCP client configuration locations:")
    print("   • Cursor IDE: ~/.cursor/mcp.json")
    print("   • General MCP: ~/.config/mcp/config.json")
    print()
    print("📄 Configuration to add:")
    print("-" * 30)


def main():
    """Main function to generate and display MCP configuration."""
    print_usage_instructions()

    config = generate_mcp_config()
    print(json.dumps(config, indent=2))

    print("-" * 30)
    print()
    print("🛠️ Available Tools:")
    print("   • detect_workspace_tools - Analyze project configuration")
    print("   • lint - Run linting with project settings")
    print("   • format - Format code with project settings")
    print("   • test - Execute tests with project settings")
    print("   • check_config_files - Verify config file presence")
    print()
    print("💡 For more examples and development setup:")
    print("   See: https://github.com/Agent-Hellboy/python-lft-mcp/tree/main/examples")
    print()
    print(
        "🎉 Ready to use! Restart your MCP client and enjoy intelligent Python tooling!"
    )


if __name__ == "__main__":
    main()
