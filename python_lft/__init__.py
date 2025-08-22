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

# Public API - conditionally import MCP-dependent modules
try:
    from .app import create_mcp
except ImportError:
    create_mcp = None
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
    "detect_tools",
    "get_config_manager",
    "get_python_files",
]

# Only add create_mcp to __all__ if it's available
if create_mcp is not None:
    __all__.append("create_mcp")
