"""MCP stdio server application factory."""

import logging

from mcp.server.fastmcp import FastMCP

from .tools_api import register_tools


logger = logging.getLogger(__name__)


def create_mcp() -> FastMCP:
    """
    Create and configure the MCP instance for stdio communication.

    Returns:
        Configured FastMCP instance for stdio transport
    """
    mcp = FastMCP(
        name="python-lft",
        dependencies=["ruff", "black", "pytest"],
    )

    # Register all MCP tools
    register_tools(mcp)

    logger.info("MCP instance created with all tools registered for stdio transport")
    return mcp
