#!/usr/bin/env python3
"""
Command-line interface for Python LFT MCP Server.
"""

import logging
import sys
from pathlib import Path


def main():
    """Main entry point for the CLI."""
    # Add the package root to Python path for development
    package_root = Path(__file__).parent.parent
    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Import and run the MCP server
    from python_lft.app import create_mcp

    # Create and run the MCP instance
    mcp = create_mcp()
    mcp.run()


if __name__ == "__main__":
    main()
