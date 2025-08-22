"""Workspace file discovery, configuration detection, and tool detection."""

import glob
import logging
import os
from pathlib import Path
from typing import Any, Optional

from ..config.constants import (
    CONFIG_FILES,
    DEFAULT_EXCLUDES,
    FORMATTER_PRIORITY,
    LINTER_PRIORITY,
    TESTER_PRIORITY,
)
from ..core.models import ToolConfig, WorkspaceTools


logger = logging.getLogger(__name__)

# Optional imports with graceful fallback
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # fallback for Python < 3.11
    except ImportError:
        tomllib = None

try:
    import yaml
except ImportError:
    yaml = None

try:
    import configparser
except ImportError:
    configparser = None


def get_python_files(target: str = "all", work_dir: Optional[str] = None) -> list[str]:
    """
    Get Python files based on target specification.

    Args:
        target: "all" for all Python files, or specific file path
        work_dir: Directory to search in (defaults to current directory)

    Returns:
        List of Python file paths
    """
    # Change to work directory if specified
    original_dir = None
    if work_dir:
        original_dir = os.getcwd()
        os.chdir(work_dir)
        logger.info(f"Changed working directory to: {work_dir}")

    try:
        if target == "all":
            # Find all Python files with smart excludes
            all_files = glob.glob("**/*.py", recursive=True)

            # Apply exclusion patterns
            filtered_files = []
            for file_path in all_files:
                excluded = False
                for pattern in DEFAULT_EXCLUDES:
                    # Convert glob pattern to path matching
                    if _matches_exclude_pattern(file_path, pattern):
                        excluded = True
                        break
                if not excluded:
                    filtered_files.append(file_path)

            logger.info(
                f"Found {len(filtered_files)} Python files (excluded {len(all_files) - len(filtered_files)})"
            )
            return sorted(filtered_files)
        else:
            # Return specific file if it exists
            if os.path.exists(target) and target.endswith(".py"):
                return [target]
            else:
                logger.warning(f"Target file not found: {target}")
                return []
    finally:
        # Restore original directory
        if original_dir:
            os.chdir(original_dir)


def _matches_exclude_pattern(file_path: str, pattern: str) -> bool:
    """Check if a file path matches an exclusion pattern."""
    # Convert glob-style pattern to simple matching
    if pattern.endswith("/*"):
        prefix = pattern[:-2]
        return file_path.startswith(prefix + "/") or file_path.startswith(prefix)
    elif "**" in pattern:
        # Handle recursive patterns
        import fnmatch

        return fnmatch.fnmatch(file_path, pattern)
    else:
        return file_path.startswith(pattern.rstrip("/"))

    # Default case: no match
    return False


def detect_tools(work_dir: Optional[str] = None) -> WorkspaceTools:
    """
    Detect available tools and configuration files in the workspace.

    Args:
        work_dir: Directory to analyze (defaults to current directory)

    Returns:
        WorkspaceTools object with detected linters, formatters, testers, and configs
    """
    # Change to work directory if specified
    original_dir = None
    if work_dir:
        original_dir = os.getcwd()
        os.chdir(work_dir)
        logger.info(f"Detecting tools in directory: {work_dir}")

    try:
        logger.info("Detecting available tools and configurations")

        # Detect configuration files
        config_files = _detect_config_files()

        # Detect tools
        linters = _detect_linters(config_files)
        formatters = _detect_formatters(config_files)
        testers = _detect_testers(config_files)

        # Create config files existence map from detected files
        config_files_exist = {name: name in config_files for name in CONFIG_FILES}

        return WorkspaceTools(
            linters=linters,
            formatters=formatters,
            testers=testers,
            config_files=config_files_exist,
        )
    finally:
        # Restore original directory
        if original_dir:
            os.chdir(original_dir)


def _detect_config_files() -> dict[str, Any]:
    """Detect and parse configuration files."""
    configs = {}

    for config_file in CONFIG_FILES:
        if os.path.exists(config_file):
            try:
                config_data = _parse_config_file(config_file)
                if config_data:
                    configs[config_file] = config_data
                    logger.info(f"Found config file: {config_file}")
            except Exception as e:
                logger.warning(f"Failed to parse {config_file}: {e}")

    return configs


def _parse_config_file(file_path: str) -> Optional[dict[str, Any]]:
    """Parse a configuration file based on its format."""
    path = Path(file_path)

    try:
        # TOML files
        if path.suffix == ".toml" and tomllib:
            with open(file_path, "rb") as f:
                return tomllib.load(f)

        # YAML files
        elif path.suffix in {".yaml", ".yml"} and yaml:
            with open(file_path) as f:
                return yaml.safe_load(f)

        # JSON files
        elif path.suffix == ".json":
            import json

            with open(file_path) as f:
                return json.load(f)

        # INI/CFG files
        elif (
            path.suffix in {".ini", ".cfg"}
            or path.name
            in {".flake8", ".pylintrc", ".style.yapf", ".yapfrc", ".coveragerc"}
        ) and configparser:
            config = configparser.ConfigParser()
            config.read(file_path)
            return {section: dict(config[section]) for section in config.sections()}

        # Python files (setup.py, conf.py)
        elif path.suffix == ".py":
            return _parse_python_config_file(file_path)

        # Requirements files
        elif "requirements" in path.name and path.suffix == ".txt":
            return _parse_requirements_file(file_path)

        # Plain text files with special handling
        elif path.name in {".gitignore", ".editorconfig", "Dockerfile"}:
            return _parse_text_config_file(file_path)

        # Pipfile (TOML-like)
        elif path.name == "Pipfile":
            with open(file_path) as f:
                content = f.read()
                return {"pipfile_content": content}

        else:
            # Unknown format
            return None

    except Exception as e:
        logger.warning(f"Failed to parse {file_path}: {e}")
        return None


def _parse_python_config_file(file_path: str) -> Optional[dict[str, Any]]:
    """Parse Python configuration files like setup.py."""
    try:
        with open(file_path) as f:
            content = f.read()

        # Extract basic information from setup.py
        config = {}
        if "setup(" in content:
            # Try to extract setup() parameters
            import re

            # Extract common setup parameters
            for param in [
                "name",
                "version",
                "description",
                "author",
                "python_requires",
            ]:
                pattern = rf'{param}\s*=\s*["\']([^"\']+)["\']'
                match = re.search(pattern, content)
                if match:
                    config[param] = match.group(1)

            # Extract install_requires
            requires_pattern = r"install_requires\s*=\s*\[(.*?)\]"
            match = re.search(requires_pattern, content, re.DOTALL)
            if match:
                requires_content = match.group(1)
                requires = [
                    req.strip().strip("\"'")
                    for req in requires_content.split(",")
                    if req.strip()
                ]
                config["install_requires"] = requires

        return (
            config if config else {"python_file": True, "content_length": len(content)}
        )

    except Exception:
        return None


def _parse_requirements_file(file_path: str) -> Optional[dict[str, Any]]:
    """Parse requirements.txt files."""
    try:
        with open(file_path) as f:
            lines = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.startswith("#")
            ]

        return {"requirements": lines, "count": len(lines), "file_type": "requirements"}
    except Exception:
        return None


def _parse_text_config_file(file_path: str) -> Optional[dict[str, Any]]:
    """Parse plain text configuration files."""
    try:
        with open(file_path) as f:
            content = f.read()

        return {
            "file_type": "text_config",
            "line_count": len(content.splitlines()),
            "content_length": len(content),
            "filename": Path(file_path).name,
        }
    except Exception:
        return None


def _detect_linters(configs: dict[str, Any]) -> list[ToolConfig]:
    """Detect configured linters by parsing config files."""
    linters = []

    for linter_name in LINTER_PRIORITY:
        # Find relevant config files
        config_files = _find_tool_configs(linter_name, configs)
        config_data = _extract_tool_config(linter_name, configs)

        # Mark as configured if found in any config file
        is_configured = bool(config_files or config_data)

        if is_configured:
            logger.info(f"Linter {linter_name} is configured in: {config_files}")

        tool_config = ToolConfig(
            name=linter_name,
            command=linter_name,  # Simple command name
            available=is_configured,  # True if configured in project
            config_files=config_files,
            config_data=config_data,
        )

        linters.append(tool_config)

    return linters


def _detect_formatters(configs: dict[str, Any]) -> list[ToolConfig]:
    """Detect configured formatters by parsing config files."""
    formatters = []

    for formatter_name in FORMATTER_PRIORITY:
        # Find relevant config files
        config_files = _find_tool_configs(formatter_name, configs)
        config_data = _extract_tool_config(formatter_name, configs)

        # Mark as configured if found in any config file
        is_configured = bool(config_files or config_data)

        if is_configured:
            logger.info(f"Formatter {formatter_name} is configured in: {config_files}")

        tool_config = ToolConfig(
            name=formatter_name,
            command=formatter_name,  # Simple command name
            available=is_configured,  # True if configured in project
            config_files=config_files,
            config_data=config_data,
        )

        formatters.append(tool_config)

    return formatters


def _detect_testers(configs: dict[str, Any]) -> list[ToolConfig]:
    """Detect configured test runners by parsing config files."""
    testers = []

    for tester_name in TESTER_PRIORITY:
        # Find relevant config files
        config_files = _find_tool_configs(tester_name, configs)
        config_data = _extract_tool_config(tester_name, configs)

        # Mark as configured if found in any config file
        is_configured = bool(config_files or config_data)

        if is_configured:
            logger.info(f"Test runner {tester_name} is configured in: {config_files}")

        tool_config = ToolConfig(
            name=tester_name,
            command=tester_name,  # Simple command name
            available=is_configured,  # True if configured in project
            config_files=config_files,
            config_data=config_data,
        )

        testers.append(tool_config)

    return testers


def _find_tool_configs(tool_name: str, configs: dict[str, Any]) -> list[str]:
    """Find configuration files relevant to a specific tool."""
    relevant_configs = []

    for config_file in configs.keys():
        if tool_name in config_file.lower():
            relevant_configs.append(config_file)
        elif (
            config_file == "pyproject.toml"
            and tool_name in str(configs[config_file]).lower()
        ):
            relevant_configs.append(config_file)
        elif (
            config_file == "setup.cfg"
            and tool_name in str(configs[config_file]).lower()
        ):
            relevant_configs.append(config_file)

    return relevant_configs


def _extract_tool_config(
    tool_name: str, configs: dict[str, Any]
) -> Optional[dict[str, Any]]:
    """Extract comprehensive configuration specific to a tool from all config files."""
    extracted_config = {}

    # Check pyproject.toml first - most comprehensive
    if "pyproject.toml" in configs:
        pyproject = configs["pyproject.toml"]
        if isinstance(pyproject, dict):
            # Look for tool.{tool_name} section
            tool_section = pyproject.get("tool", {}).get(tool_name)
            if tool_section:
                extracted_config.update(tool_section)

    # Check setup.cfg
    if "setup.cfg" in configs:
        setup_cfg = configs["setup.cfg"]
        if isinstance(setup_cfg, dict):
            # Look for tool-specific sections
            for section_name, section_data in setup_cfg.items():
                if tool_name in section_name.lower():
                    extracted_config.update(section_data)

    # Check tox.ini
    if "tox.ini" in configs:
        tox_ini = configs["tox.ini"]
        if isinstance(tox_ini, dict):
            for section_name, section_data in tox_ini.items():
                if tool_name in section_name.lower():
                    extracted_config.update(section_data)

    # Check tool-specific config files
    for config_file, config_data in configs.items():
        if tool_name in config_file.lower() and isinstance(config_data, dict):
            extracted_config.update(config_data)

    return extracted_config if extracted_config else None
