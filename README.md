# Python LFT (Lint, Format, Test) - MCP Server

A modern, modular Python development tools package that exposes linting, formatting, and testing capabilities via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Built with clean architecture and modern design patterns for professional development workflows.

[![GitHub Repository](https://img.shields.io/badge/GitHub-Agent--Hellboy%2Fpython--lft--mcp-blue.svg)](https://github.com/Agent-Hellboy/python-lft-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Agent-Hellboy/python-lft-mcp/blob/main/LICENSE)

[![Tests](https://github.com/Agent-Hellboy/python-lft-mcp/workflows/Tests/badge.svg)](https://github.com/Agent-Hellboy/python-lft-mcp/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/Agent-Hellboy/python-lft-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/Agent-Hellboy/python-lft-mcp)

A comprehensive MCP server that provides intelligent linting, formatting, and testing capabilities for Python projects. It automatically detects project configurations and enables LLMs to make smart decisions about code quality tools.

## Features

- **Comprehensive Config Detection** - Analyzes 70+ Python ecosystem config files
- **Smart Tool Integration** - Supports ruff, black, pytest, mypy, pylint, and more
- **LLM-Optimized** - Provides detailed configuration data for intelligent tool selection
- **Cross-Project Support** - Works with any Python project structure
- **Fast & Reliable** - Built with modern async Python and MCP protocols

## Quick Start

### Installation

```bash
# Install from PyPI (when published)
pip install python-lft-mcp

# Or install with all optional tool dependencies
pip install python-lft-mcp[tools]
```

### MCP Client Configuration

After installation, generate your MCP configuration:

```bash
# Generate configuration for your MCP client
python-lft-config
```

This will display the configuration you need to add to your MCP client.

#### Quick Configuration for Cursor IDE
Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "python-lft": {
      "command": "python",
      "args": ["-m", "python_lft"],
      "description": "Python LFT MCP Server"
    }
  }
}
```

#### For Other MCP Clients
- Run `python-lft-config` for complete instructions
- See `examples/mcp-config.json` for more configuration options

### Development Installation

```bash
# Clone the repository  
git clone https://github.com/Agent-Hellboy/python-lft-mcp.git
cd python-lft-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

For development configuration, see `examples/README.md`.

## Usage

### 1. Detect Project Configuration
```python
# LLM calls this first to understand the project
detect_workspace_tools(work_dir="/path/to/project")
```

### 2. Execute Tools with Project Settings
```python
# LLM uses the detected configuration
lint(
    target="all",
    exact_tool="ruff", 
    tool_config={"line-length": 88, "target-version": "py39"},
    work_dir="/path/to/project"
)

format_code(
    exact_tool="black",
    tool_config={"line-length": 88, "target-version": ["py39"]},
    work_dir="/path/to/project"
)

test(
    exact_tool="pytest",
    tool_config={"testpaths": ["tests"], "addopts": "-v"},
    work_dir="/path/to/project"
)
```

## Supported Tools

### Linters
- **ruff** - Fast Python linter
- **flake8** - Style guide enforcement  
- **pylint** - Code analysis
- **mypy** - Static type checking
- **bandit** - Security linting
- **pydocstyle** - Docstring conventions

### Formatters  
- **black** - Code formatting
- **ruff** - Fast formatting
- **isort** - Import sorting
- **autopep8** - PEP 8 formatting
- **yapf** - Code formatting

### Test Runners
- **pytest** - Testing framework
- **nose2** - Unit testing
- **unittest** - Built-in testing

## Supported Configuration Files

- `pyproject.toml` - Modern Python project config
- `setup.cfg` - Legacy setuptools config  
- `tox.ini` - Testing automation
- `pytest.ini` - Pytest configuration
- `.flake8` - Flake8 settings
- `.pylintrc` - Pylint configuration
- `mypy.ini` - MyPy settings
- `requirements.txt` - Dependencies
- `.pre-commit-config.yaml` - Pre-commit hooks
- And 60+ more Python ecosystem configs!

## Development

### Setup Development Environment
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (if available)
pre-commit install
```

### Development Workflows with Tox

We use [tox](https://tox.wiki/) for standardized development workflows:

```bash
# Run tests across all supported Python versions
tox

# Run specific environments
tox -e lint          # Run linting with ruff
tox -e format        # Format code with ruff (includes import sorting)
tox -e format-check  # Check formatting without changes
tox -e type          # Type checking with mypy
tox -e coverage      # Run tests with coverage reporting

# Run comprehensive testing
tox -e all           # Lint + format-check + type + test + coverage

# Test specific Python version
tox -e py39          # Test with Python 3.9
tox -e py312         # Test with Python 3.12

# Clean build artifacts
tox -e clean

# Build package for distribution
tox -e build
```

### Manual Tool Usage
```bash
# Run tests
pytest

# Run linting
ruff check .

# Type checking
mypy python_lft/

# Format code  
ruff check --fix .  # Fix linting issues and sort imports
ruff format .       # Format code

# Run tests with coverage
pytest --cov=python_lft
```

### Architecture

```
python_lft/
├── app.py              # MCP server creation
├── tools_api.py        # MCP tool definitions  
├── services/
│   ├── workspace.py    # Configuration detection
│   ├── orchestrator.py # Tool execution coordination
│   └── runners.py      # Command execution
├── executors/          # Tool-specific executors
├── core/              # Core models and interfaces
└── config/            # Constants and configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite: `tox -e all`
6. Submit a pull request

### CI/CD

The project uses GitHub Actions for continuous integration:

- **Lint**: Runs `ruff check` on every push/PR
- **Tests**: Runs test suite across Python 3.9-3.12 on every push/PR  
- **CI**: Comprehensive quality checks (lint + format + type + test + build)
- **Publish**: Automatically publishes to PyPI and GitHub releases on version tags

All checks must pass before merging pull requests.

## License

MIT License - see [LICENSE](https://github.com/Agent-Hellboy/python-lft-mcp/blob/main/LICENSE) file for details.

## Repository

For the latest updates, issues, and contributions, visit: [https://github.com/Agent-Hellboy/python-lft-mcp](https://github.com/Agent-Hellboy/python-lft-mcp)