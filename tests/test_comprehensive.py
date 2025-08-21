"""Comprehensive tests for Python LFT components."""

from unittest.mock import mock_open, patch

import pytest

from python_lft.core.models import CommandResult, ToolConfig, ToolStatus, WorkspaceTools
from python_lft.executors.factories import (
    FormatterFactory,
    LinterFactory,
    TesterFactory,
)
from python_lft.services.orchestrator import ToolOrchestrator
from python_lft.services.runners import combine_results
from python_lft.services.workspace import (
    _detect_config_files,
    _matches_exclude_pattern,
    _parse_config_file,
    detect_tools,
    get_python_files,
)


class TestToolOrchestrator:
    """Test the ToolOrchestrator functionality."""

    def test_orchestrator_creation(self):
        """Test ToolOrchestrator can be created."""
        orchestrator = ToolOrchestrator()
        assert orchestrator is not None

    def test_get_available_linters(self):
        """Test getting available linters."""
        orchestrator = ToolOrchestrator()
        with patch("python_lft.services.workspace.detect_tools") as mock_detect:
            mock_detect.return_value = WorkspaceTools(
                linters=[
                    ToolConfig(
                        name="ruff",
                        command="ruff",
                        available=True,
                        config_files=["pyproject.toml"],
                    )
                ],
                formatters=[],
                testers=[],
                config_files={},
            )

            result = orchestrator._get_available_linters()
            assert "ruff" in result


class TestFactories:
    """Test executor factories."""

    def test_linter_factory_creation(self):
        """Test LinterFactory creates executors."""
        factory = LinterFactory()
        supported = factory.get_supported_tools()
        assert "ruff" in supported
        assert "flake8" in supported
        assert "pylint" in supported

    def test_formatter_factory_creation(self):
        """Test FormatterFactory creates executors."""
        factory = FormatterFactory()
        supported = factory.get_supported_tools()
        assert "black" in supported
        assert "ruff" in supported
        assert "isort" in supported

    def test_tester_factory_creation(self):
        """Test TesterFactory creates executors."""
        factory = TesterFactory()
        supported = factory.get_supported_tools()
        assert "pytest" in supported
        assert "unittest" in supported


class TestCommandResult:
    """Test CommandResult functionality."""

    def test_command_result_success_property(self):
        """Test CommandResult success property."""
        # Successful command
        result = CommandResult(exit_code=0, stdout="output", stderr="")
        assert result.success is True

        # Failed command
        result = CommandResult(exit_code=1, stdout="", stderr="error")
        assert result.success is False

    def test_command_result_str_representation(self):
        """Test CommandResult string representation."""
        result = CommandResult(exit_code=0, stdout="test output", stderr="")
        str_repr = str(result)
        assert "exit_code=0" in str_repr
        assert "test output" in str_repr


class TestConfigFileParsing:
    """Test configuration file parsing."""

    def test_parse_toml_config(self):
        """Test parsing TOML configuration."""
        toml_content = b"""
[tool.ruff]
line-length = 88
target-version = "py39"
"""
        with patch("builtins.open", mock_open(read_data=toml_content)):
            with patch("python_lft.services.workspace.tomllib") as mock_tomllib:
                mock_tomllib.load.return_value = {
                    "tool": {"ruff": {"line-length": 88, "target-version": "py39"}}
                }
                result = _parse_config_file("pyproject.toml")

        assert result is not None
        assert "tool" in result
        assert "ruff" in result["tool"]

    def test_parse_yaml_config(self):
        """Test parsing YAML configuration."""
        yaml_content = """
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
"""
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            with patch("yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "repos": [{"repo": "https://github.com/psf/black"}]
                }
                result = _parse_config_file(".pre-commit-config.yaml")

        assert result is not None

    def test_parse_invalid_config(self):
        """Test parsing invalid configuration."""
        result = _parse_config_file("nonexistent.conf")
        assert result is None


class TestWorkspaceDetection:
    """Test workspace detection functionality."""

    def test_detect_tools_with_configs(self):
        """Test detecting tools with configuration."""
        mock_config = {
            "pyproject.toml": {
                "tool": {
                    "ruff": {"line-length": 88},
                    "black": {"line-length": 88},
                    "pytest": {"testpaths": ["tests"]},
                }
            }
        }

        with patch(
            "python_lft.services.workspace._detect_config_files",
            return_value=mock_config,
        ):
            result = detect_tools()

            # Should find configured tools
            linter_names = [tool.name for tool in result.linters]
            formatter_names = [tool.name for tool in result.formatters]
            tester_names = [tool.name for tool in result.testers]

            assert "ruff" in linter_names
            assert "black" in formatter_names
            assert "pytest" in tester_names

    def test_detect_tools_without_configs(self):
        """Test detecting tools without configuration."""
        with patch(
            "python_lft.services.workspace._detect_config_files", return_value={}
        ):
            result = detect_tools()

            # Should return empty lists when no config
            assert isinstance(result.linters, list)
            assert isinstance(result.formatters, list)
            assert isinstance(result.testers, list)


class TestFileMatching:
    """Test file pattern matching."""

    def test_matches_exclude_pattern_venv(self):
        """Test venv exclusion patterns."""
        assert _matches_exclude_pattern("venv/lib/package.py", "venv/*")
        assert _matches_exclude_pattern(".venv/lib/package.py", ".venv/*")
        assert not _matches_exclude_pattern("src/venv.py", "venv/*")

    def test_matches_exclude_pattern_pycache(self):
        """Test __pycache__ exclusion patterns."""
        assert _matches_exclude_pattern("src/__pycache__/file.pyc", "**/__pycache__/**")
        assert _matches_exclude_pattern(
            "deep/nested/__pycache__/cache.py", "**/__pycache__/**"
        )
        assert not _matches_exclude_pattern("src/main.py", "**/__pycache__/**")

    def test_matches_exclude_pattern_git(self):
        """Test .git exclusion patterns."""
        assert _matches_exclude_pattern(".git/config", ".git/*")
        assert _matches_exclude_pattern(".git/hooks/pre-commit", ".git/*")
        assert not _matches_exclude_pattern("src/.gitignore", ".git/*")

    def test_matches_exclude_pattern_exact(self):
        """Test exact pattern matching."""
        assert _matches_exclude_pattern("build/temp.py", "build")
        assert _matches_exclude_pattern("build/lib/module.py", "build")
        assert not _matches_exclude_pattern("rebuild.py", "build")


class TestPythonFileDiscovery:
    """Test Python file discovery."""

    def test_get_python_files_specific_file(self, tmp_path):
        """Test getting a specific Python file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        result = get_python_files(str(test_file))
        assert str(test_file) in result

    def test_get_python_files_non_python(self):
        """Test getting a non-Python file returns empty."""
        with patch("os.path.exists", return_value=True):
            result = get_python_files("README.md")
        assert result == []

    def test_get_python_files_nonexistent(self):
        """Test getting a nonexistent file."""
        with patch("os.path.exists", return_value=False):
            result = get_python_files("nonexistent.py")
        assert result == []

    @patch("glob.glob")
    def test_get_python_files_all_with_exclusions(self, mock_glob):
        """Test getting all Python files with exclusions."""
        mock_glob.return_value = [
            "main.py",
            "src/utils.py",
            "venv/lib/python3.12/package.py",
            "tests/test_main.py",
            ".venv/package.py",
            "build/temp.py",
        ]

        result = get_python_files("all")

        # Should exclude venv, .venv, build
        expected = ["main.py", "src/utils.py", "tests/test_main.py"]
        assert sorted(result) == sorted(expected)


class TestAsyncRunners:
    """Test async command runners."""

    @pytest.mark.asyncio
    async def test_combine_results(self):
        """Test combining command results."""
        results = [
            CommandResult(exit_code=0, stdout="output1", stderr=""),
            CommandResult(exit_code=0, stdout="output2", stderr=""),
            CommandResult(exit_code=1, stdout="", stderr="error1"),
        ]

        combined = combine_results(results)

        assert combined.exit_code == 1  # Should be highest exit code
        assert "output1" in combined.stdout
        assert "output2" in combined.stdout
        assert "error1" in combined.stderr

    @pytest.mark.asyncio
    async def test_combine_results_empty(self):
        """Test combining empty results."""
        combined = combine_results([])

        assert combined.exit_code == 0
        assert combined.stdout == ""
        assert combined.stderr == ""


class TestToolModels:
    """Test tool-related models."""

    def test_tool_status_enum(self):
        """Test ToolStatus enum values."""
        assert ToolStatus.SUCCESS.value == "success"
        assert ToolStatus.WARNING.value == "warning"
        assert ToolStatus.ERROR.value == "error"

    def test_workspace_tools_best_methods(self):
        """Test WorkspaceTools best tool selection."""
        tools = WorkspaceTools(
            linters=[
                ToolConfig(
                    name="ruff", command="ruff", available=True, config_files=[]
                ),
                ToolConfig(
                    name="flake8", command="flake8", available=True, config_files=[]
                ),
            ],
            formatters=[
                ToolConfig(
                    name="black", command="black", available=True, config_files=[]
                ),
            ],
            testers=[
                ToolConfig(
                    name="pytest", command="pytest", available=True, config_files=[]
                ),
            ],
            config_files={},
        )

        # Should return first available tool
        best_linter = tools.get_best_linter()
        assert best_linter is not None
        assert best_linter.name == "ruff"

        best_formatter = tools.get_best_formatter()
        assert best_formatter is not None
        assert best_formatter.name == "black"

        best_tester = tools.get_best_tester()
        assert best_tester is not None
        assert best_tester.name == "pytest"

    def test_workspace_tools_no_available_tools(self):
        """Test WorkspaceTools with no available tools."""
        tools = WorkspaceTools(linters=[], formatters=[], testers=[], config_files={})

        assert tools.get_best_linter() is None
        assert tools.get_best_formatter() is None
        assert tools.get_best_tester() is None


class TestConfigDetection:
    """Test configuration file detection."""

    @patch("os.path.exists")
    @patch("python_lft.services.workspace._parse_config_file")
    def test_detect_config_files(self, mock_parse, mock_exists):
        """Test detecting configuration files."""

        # Mock some config files existing
        def exists_side_effect(path):
            return path in ["pyproject.toml", "setup.cfg", ".flake8"]

        mock_exists.side_effect = exists_side_effect

        def parse_side_effect(path):
            if path == "pyproject.toml":
                return {"tool": {"ruff": {"line-length": 88}}}
            elif path == "setup.cfg":
                return {"flake8": {"max-line-length": "88"}}
            elif path == ".flake8":
                return {"max-line-length": "88"}
            return None

        mock_parse.side_effect = parse_side_effect

        result = _detect_config_files()

        assert "pyproject.toml" in result
        assert "setup.cfg" in result
        assert ".flake8" in result


if __name__ == "__main__":
    pytest.main([__file__])
