"""
Python LFT (Lint, Format, Test) - MCP Server

A modular Python development tools package that exposes linting, formatting,
and testing capabilities via Model Context Protocol (MCP).

Design Patterns Used:
- Strategy Pattern: Tool execution strategies
- Factory Pattern: Tool executor creation
- Abstract Base Classes: Extensible interfaces
- Dependency Injection: Configuration management
- Command Pattern: Tool operations
"""

__version__ = "1.0.0"
__author__ = "Python LFT Contributors"

# Public API
from .app import create_mcp
from .core.config import configure, get_config_manager
from .core.models import ToolConfig, ToolResult, ToolStatus, WorkspaceTools
from .services.orchestrator import ToolOrchestrator
from .services.workspace import detect_tools, get_python_files


__all__ = [
    "ToolConfig",
    # Core functionality
    "ToolOrchestrator",
    "ToolResult",
    # Models
    "ToolStatus",
    "WorkspaceTools",
    # Configuration
    "configure",
    # MCP creation
    "create_mcp",
    "detect_tools",
    "get_config_manager",
    "get_python_files",
]
