# Configuration Examples

This directory contains example configurations for using the Python LFT MCP Server.

## MCP Client Configuration

After installing the package, add the configuration to your MCP client:

### For Cursor IDE
Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "python-lft": {
      "command": "python",
      "args": ["-m", "python_lft"],
      "description": "Python Lint, Format, Test (LFT) - Intelligent Python development tools",
      "version": "1.0.0"
    }
  }
}
```

### For Other MCP Clients
Add to your client's configuration file (location varies by client):

```json
{
  "mcpServers": {
    "python-lft": {
      "command": "python",
      "args": ["-m", "python_lft"],
      "description": "Python LFT MCP Server",
      "version": "1.0.0"
    }
  }
}
```

## Development Configuration

If you're running from source (development mode), use this configuration instead:

```json
{
  "mcpServers": {
    "python-lft": {
      "command": "/path/to/python-lft-mcp/venv/bin/python",
      "args": ["/path/to/python-lft-mcp/main.py"],
      "cwd": "/path/to/python-lft-mcp",
      "env": {
        "VIRTUAL_ENV": "/path/to/python-lft-mcp/venv",
        "PYTHONPATH": "/path/to/python-lft-mcp"
      },
      "description": "Python LFT MCP Server (development mode)",
      "version": "1.0.0"
    }
  }
}
```

## Installation Steps

1. **Install the package:**
   ```bash
   pip install python-lft-mcp
   ```

2. **Add configuration to your MCP client** (see examples above)

3. **Restart your MCP client** to load the new server

4. **Verify installation** by checking if the `python-lft` tools are available in your MCP client

## Available Tools

Once configured, you'll have access to these tools:

- `detect_workspace_tools` - Analyze project configuration
- `lint` - Run linting with project settings  
- `format` - Format code with project settings
- `test` - Execute tests with project settings
- `check_config_files` - Verify config file presence

## Repository

For the latest updates and documentation, visit: [https://github.com/Agent-Hellboy/python-lft-mcp](https://github.com/Agent-Hellboy/python-lft-mcp)
