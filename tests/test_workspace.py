"""Tests for workspace module."""

from unittest.mock import mock_open, patch

from python_lft.services.workspace import (
    _detect_config_files,
    _matches_exclude_pattern,
    _parse_config_file,
    detect_tools,
    get_python_files,
)


class TestGetPythonFiles:
    """Test file discovery functionality."""

    def test_get_specific_file_exists(self, tmp_path):
        """Test getting a specific Python file that exists."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        with patch("os.path.exists", return_value=True):
            result = get_python_files(str(test_file))

        assert result == [str(test_file)]

    def test_get_specific_file_not_exists(self):
        """Test getting a specific file that doesn't exist."""
        with patch("os.path.exists", return_value=False):
            result = get_python_files("nonexistent.py")

        assert result == []

    def test_get_specific_non_python_file(self):
        """Test getting a non-Python file."""
        with patch("os.path.exists", return_value=True):
            result = get_python_files("README.md")

        assert result == []

    @patch("glob.glob")
    def test_get_all_files_with_excludes(self, mock_glob):
        """Test getting all files with exclusion patterns."""
        mock_glob.return_value = [
            "main.py",
            "src/utils.py",
            "venv/lib/python3.12/site-packages/package.py",
            "tests/test_main.py",
            ".venv/lib/package.py",
            "build/temp.py",
        ]

        result = get_python_files("all")

        # Should exclude venv, .venv, and build files
        expected = ["main.py", "src/utils.py", "tests/test_main.py"]
        assert sorted(result) == sorted(expected)


class TestExcludePatterns:
    """Test exclusion pattern matching."""

    def test_matches_simple_prefix(self):
        """Test simple prefix matching."""
        assert _matches_exclude_pattern("venv/lib/package.py", "venv/*")
        assert _matches_exclude_pattern("venv/package.py", "venv/*")
        assert not _matches_exclude_pattern("src/venv.py", "venv/*")

    def test_matches_recursive_pattern(self):
        """Test recursive pattern matching."""
        assert _matches_exclude_pattern(
            "any/path/__pycache__/file.py", "**/__pycache__/**"
        )
        assert _matches_exclude_pattern(
            "deep/nested/__pycache__/cache.py", "**/__pycache__/**"
        )
        assert not _matches_exclude_pattern("src/main.py", "**/__pycache__/**")

    def test_matches_exact_pattern(self):
        """Test exact pattern matching."""
        assert _matches_exclude_pattern(".git/config", ".git/*")
        assert not _matches_exclude_pattern("src/.git_file", ".git/*")


class TestConfigDetection:
    """Test configuration file detection."""

    @patch("os.path.exists")
    @patch("python_lft.services.workspace._parse_config_file")
    def test_detect_existing_configs(self, mock_parse, mock_exists):
        """Test detecting existing config files."""
        mock_exists.side_effect = lambda x: x in ["pyproject.toml", "pytest.ini"]
        mock_parse.return_value = {"test": "config"}

        result = _detect_config_files()

        assert "pyproject.toml" in result
        assert "pytest.ini" in result
        assert len(result) == 2

    @patch("os.path.exists", return_value=False)
    def test_detect_no_configs(self, mock_exists):
        """Test when no config files exist."""
        result = _detect_config_files()
        assert result == {}


class TestConfigParsing:
    """Test configuration file parsing."""

    def test_parse_toml_file(self):
        """Test parsing TOML files."""
        toml_content = b"[tool.black]\nline-length = 88"

        with patch("builtins.open", mock_open(read_data=toml_content)):
            with patch("python_lft.services.workspace.tomllib") as mock_tomllib:
                mock_tomllib.load.return_value = {
                    "tool": {"black": {"line-length": 88}}
                }

                result = _parse_config_file("pyproject.toml")

                assert result == {"tool": {"black": {"line-length": 88}}}

    def test_parse_yaml_file(self):
        """Test parsing YAML files."""
        with patch("builtins.open", mock_open(read_data="test: value")):
            with patch("python_lft.services.workspace.yaml") as mock_yaml:
                mock_yaml.safe_load.return_value = {"test": "value"}

                result = _parse_config_file("config.yaml")

                assert result == {"test": "value"}

    def test_parse_unsupported_file(self):
        """Test parsing unsupported file types."""
        result = _parse_config_file("unknown.xyz")
        assert result is None


class TestToolDetection:
    """Test tool detection functionality."""

    def test_detect_configured_tools(self):
        """Test detecting configured tools (not installed tools)."""
        # Mock configuration files with tool settings
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

        # Check that configured tools are detected as available
        assert any(tool.name == "ruff" and tool.available for tool in result.linters)
        assert any(
            tool.name == "black" and tool.available for tool in result.formatters
        )
        assert any(tool.name == "pytest" and tool.available for tool in result.testers)

    def test_detect_no_tools(self):
        """Test when no tools are configured."""

        with patch(
            "python_lft.services.workspace._detect_config_files", return_value={}
        ):
            result = detect_tools()

        # All tools should be marked as unavailable
        assert not any(tool.available for tool in result.linters)
        assert not any(tool.available for tool in result.formatters)
        assert not any(tool.available for tool in result.testers)
