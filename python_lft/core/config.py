"""Configuration management for Python LFT."""

from dataclasses import dataclass, field
from typing import Any, Optional

from ..core.formatters import CompactFormatter, StandardFormatter
from ..core.interfaces import ResultFormatter


@dataclass
class LftConfig:
    """Configuration for Python LFT operations."""

    # Output formatting
    formatter_type: str = "standard"  # "standard" or "compact"

    # Tool execution
    default_timeout: float = 300.0
    quick_timeout: float = 30.0
    max_files_per_batch: int = 200

    # Tool preferences (can be overridden by tool_name parameter)
    preferred_linter: Optional[str] = None
    preferred_formatter: Optional[str] = None
    preferred_tester: Optional[str] = None

    # Additional configuration
    extra_config: dict[str, Any] = field(default_factory=dict)

    def get_formatter(self) -> ResultFormatter:
        """Get the configured result formatter."""
        if self.formatter_type == "compact":
            return CompactFormatter()
        else:
            return StandardFormatter()


class ConfigManager:
    """Manages configuration for Python LFT."""

    def __init__(self, config: Optional[LftConfig] = None):
        self._config = config or LftConfig()

    @property
    def config(self) -> LftConfig:
        """Get the current configuration."""
        return self._config

    def update_config(self, **kwargs) -> None:
        """Update configuration values."""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)

    def get_formatter(self) -> ResultFormatter:
        """Get the configured result formatter."""
        return self._config.get_formatter()


# Global configuration manager instance
_config_manager = ConfigManager()


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager."""
    return _config_manager


def configure(**kwargs) -> None:
    """Configure Python LFT globally."""
    _config_manager.update_config(**kwargs)
