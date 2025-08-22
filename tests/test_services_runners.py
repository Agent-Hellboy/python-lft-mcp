"""Tests for python_lft.services.runners module."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from python_lft.core.models import CommandResult
from python_lft.services.runners import combine_results, run, run_chunked


class TestRunners:
    """Test runners module functionality."""

    @pytest.mark.asyncio
    async def test_run_success(self):
        """Test successful command execution."""
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = AsyncMock()
            mock_process.communicate.return_value = (b"output", b"")
            mock_process.returncode = 0
            mock_subprocess.return_value = mock_process

            result = await run(["echo", "hello"])

            assert result.exit_code == 0
            assert result.stdout == "output"
            assert result.stderr == ""
            assert result.success is True

    @pytest.mark.asyncio
    async def test_run_failure(self):
        """Test failed command execution."""
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = AsyncMock()
            mock_process.communicate.return_value = (b"", b"error")
            mock_process.returncode = 1
            mock_subprocess.return_value = mock_process

            result = await run(["false"])

            assert result.exit_code == 1
            assert result.stderr == "error"
            assert result.success is False

    @pytest.mark.asyncio
    async def test_run_with_cwd(self):
        """Test command execution with working directory."""
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = AsyncMock()
            mock_process.communicate.return_value = (b"output", b"")
            mock_process.returncode = 0
            mock_subprocess.return_value = mock_process

            result = await run(["pwd"], cwd="/tmp")

            assert result.exit_code == 0
            # The cwd parameter should be passed to subprocess
            mock_subprocess.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_chunked_empty(self):
        """Test chunked execution with empty file list."""
        result_list = await run_chunked(["ruff", "check"], [])
        assert result_list == []

    @pytest.mark.asyncio
    async def test_run_chunked_single_chunk(self):
        """Test chunked execution with single chunk."""
        with patch("python_lft.services.runners.run") as mock_run:
            mock_run.return_value = CommandResult(
                exit_code=0, stdout="output", stderr=""
            )

            files = ["file1.py", "file2.py"]
            result_list = await run_chunked(["ruff", "check"], files, chunk_size=10)

            # Should call run only once with all files
            assert mock_run.call_count == 1
            assert len(result_list) == 1

    def test_combine_results_success(self):
        """Test combining successful results."""
        results = [
            CommandResult(exit_code=0, stdout="output1", stderr=""),
            CommandResult(exit_code=0, stdout="output2", stderr=""),
        ]

        combined = combine_results(results)

        assert combined.exit_code == 0
        assert "output1" in combined.stdout
        assert "output2" in combined.stdout
        assert combined.success is True

    def test_combine_results_with_errors(self):
        """Test combining results with errors."""
        results = [
            CommandResult(exit_code=0, stdout="success", stderr=""),
            CommandResult(exit_code=1, stdout="", stderr="error"),
        ]

        combined = combine_results(results)

        assert combined.exit_code == 1  # Highest exit code
        assert "success" in combined.stdout
        assert "error" in combined.stderr
        assert combined.success is False

    def test_combine_results_empty(self):
        """Test combining empty results list."""
        combined = combine_results([])

        assert combined.exit_code == 0
        assert combined.stdout == ""
        assert combined.stderr == ""
        assert combined.success is True
