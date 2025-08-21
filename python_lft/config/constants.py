"""Constants for Python LFT configuration and tool detection."""

# File patterns to exclude when scanning for Python files
DEFAULT_EXCLUDES: list[str] = [
    "v/*",
    "venv/*",
    ".venv/*",
    "env/*",
    ".env/*",
    "**/site-packages/**",
    "**/__pycache__/**",
    ".git/*",
    "build/*",
    "dist/*",
    ".tox/*",
]

# Comprehensive Python ecosystem configuration files (in detection order)
CONFIG_FILES: list[str] = [
    # Main project configuration
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
    # Tool-specific TOML configs
    "ruff.toml",
    ".ruff.toml",
    "black.toml",
    ".black.toml",
    # Testing configurations
    "pytest.ini",
    ".pytest.ini",
    "tox.ini",
    "nose2.cfg",
    "unittest.cfg",
    # Linting configurations
    ".flake8",
    "flake8.ini",
    ".pylintrc",
    "pylintrc",
    ".pylint",
    "mypy.ini",
    ".mypy.ini",
    "bandit.yaml",
    "bandit.yml",
    ".bandit",
    ".bandit.yaml",
    ".bandit.yml",
    # Formatting configurations
    ".isort.cfg",
    "isort.cfg",
    ".style.yapf",
    "yapf.ini",
    ".yapfrc",
    # Coverage and quality
    ".coveragerc",
    "coverage.ini",
    ".coverage",
    # Pre-commit and CI/CD
    ".pre-commit-config.yaml",
    ".pre-commit-config.yml",
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    # Documentation
    "mkdocs.yml",
    "mkdocs.yaml",
    "conf.py",  # Sphinx
    # Dependency management
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-test.txt",
    "dev-requirements.txt",
    "test-requirements.txt",
    "Pipfile",
    "poetry.lock",
    "conda-environment.yml",
    "environment.yml",
    # Version control and git
    ".gitignore",
    ".gitattributes",
    # Editor configurations
    ".editorconfig",
    ".vscode/settings.json",
    # Docker and deployment
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
]

# Tool selection priorities
LINTER_PRIORITY: list[str] = [
    "ruff",
    "flake8",
    "pylint",
    "mypy",
    "pydocstyle",
    "bandit",
]

FORMATTER_PRIORITY: list[str] = [
    "black",
    "ruff",
    "isort",
    "autopep8",
    "yapf",
]

TESTER_PRIORITY: list[str] = [
    "pytest",
    "nose2",
    "unittest",
]

# Default tools (when available)
DEFAULT_LINTER = "ruff"
DEFAULT_FORMATTER = "black"
DEFAULT_TESTER = "pytest"

# Command timeouts (in seconds)
DEFAULT_TIMEOUT = 300.0
QUICK_TIMEOUT = 30.0

# File batching limits (to avoid command line length limits)
MAX_FILES_PER_BATCH = 200
