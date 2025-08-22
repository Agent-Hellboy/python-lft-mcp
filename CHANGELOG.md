# Changelog

All notable changes to the Python LFT MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-01

### Initial Release

#### Added
- **Core MCP Server**: Full-featured Model Context Protocol server for Python development tools
- **Comprehensive Tool Detection**: Support for 70+ Python ecosystem configuration files
- **Smart Configuration Parsing**: Automatic detection of linting, formatting, and testing tools
- **Generic Tool Interface**: LLM-optimized tool calls with configurable parameters
- **Work Directory Support**: Cross-project analysis and execution capabilities

#### Tools
- `detect_workspace_tools` - Analyze project configuration and detect available tools
- `lint` - Run linting tools with project-specific configurations
- `format` - Format code using project-specific settings  
- `test` - Execute tests with project-specific configurations
- `check_config_files` - Verify presence of common Python config files

#### Supported Tools
- **Linters**: ruff, flake8, pylint, mypy, bandit, pydocstyle
- **Formatters**: black, ruff, isort, autopep8, yapf
- **Testers**: pytest, nose2, unittest

#### Configuration Files
- Modern: `pyproject.toml`, `setup.cfg`, `tox.ini`
- Tool-specific: `.flake8`, `.pylintrc`, `mypy.ini`, `pytest.ini`
- Dependencies: `requirements.txt`, `Pipfile`, `setup.py`
- CI/CD: `.pre-commit-config.yaml`, GitHub Actions configs
- Documentation: `mkdocs.yml`, Sphinx configs
- And 60+ more Python ecosystem configurations

#### Package Features
- **Easy Installation**: `pip install python-lft-mcp`
- **Configuration Generator**: `python-lft-config` command for MCP client setup
- **CLI Entry Points**: Multiple ways to run the server
- **Type Safety**: Full type hints with `py.typed` marker
- **Professional Structure**: Complete package metadata and documentation

#### Architecture
- **Clean Design**: Strategy and Factory patterns
- **Modular Structure**: Separate concerns for detection, orchestration, and execution
- **Async Support**: Built on modern MCP protocol standards
- **Error Handling**: Comprehensive error reporting and debugging
- **Cross-Platform**: Works on Linux, macOS, and Windows

### Technical Details
- **Python**: Requires Python 3.9+
- **MCP Protocol**: Compatible with MCP 0.9.0+
- **Dependencies**: Minimal core dependencies (mcp, PyYAML, pytest-asyncio)
- **Optional Tools**: All development tools are optional dependencies
- **Stdio Transport**: Direct stdio communication for optimal performance

### Documentation
- Comprehensive README with installation and usage examples
- Configuration examples for popular MCP clients
- Development setup instructions
- Complete API documentation

### Use Cases
- **IDE Integration**: Enhanced Python development in MCP-compatible IDEs
- **Code Quality**: Automated linting and formatting with intelligent configuration detection
- **Project Analysis**: Understand and work with any Python project structure
- **Testing Automation**: Run tests with project-specific settings
- **LLM-Powered Development**: Enable AI assistants to make smart tool decisions

### CI/CD
- **GitHub Actions**: Complete CI/CD pipeline with lint, test, and publish workflows
- **Multi-Python Testing**: Automated testing across Python 3.9-3.12
- **Code Coverage**: Codecov integration for coverage reporting
- **Automated Publishing**: PyPI and GitHub releases on version tags
- **Dependabot**: Automated dependency updates with auto-merge for patches/minor updates

---

## Repository

**GitHub**: [https://github.com/Agent-Hellboy/python-lft-mcp](https://github.com/Agent-Hellboy/python-lft-mcp)

## License

**MIT License**: [LICENSE](https://github.com/Agent-Hellboy/python-lft-mcp/blob/main/LICENSE)
