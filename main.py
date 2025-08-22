#!/usr/bin/env python3
"""
Python LFT MCP Server - Main entry point for stdio integration.

This module provides the main entry point for running the Python LFT MCP server
in stdio mode for integration with Cursor and other MCP clients.
"""

import logging

from python_lft.app import create_mcp


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create the MCP instance
mcp = create_mcp()

if __name__ == "__main__":
    # For MCP stdio integration with Cursor
    mcp.run()
