"""Async subprocess execution utilities with timeouts and safe output handling."""

import asyncio
import logging
from typing import Optional

from ..config.constants import DEFAULT_TIMEOUT
from ..core.models import CommandResult


logger = logging.getLogger(__name__)


async def run(
    cmd: list[str],
    timeout: Optional[float] = None,
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
) -> CommandResult:
    """
    Run a command asynchronously with timeout and safe output handling.

    Args:
        cmd: Command and arguments as list
        timeout: Timeout in seconds (defaults to DEFAULT_TIMEOUT)
        cwd: Working directory for command
        env: Environment variables

    Returns:
        CommandResult with exit code, stdout, stderr
    """
    if timeout is None:
        timeout = DEFAULT_TIMEOUT

    logger.info(f"Running command: {' '.join(cmd)}")

    try:
        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env,
        )

        # Wait for completion with timeout
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            stdout = (
                stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
            )
            stderr = (
                stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
            )
            exit_code = process.returncode or 0

            return CommandResult(exit_code=exit_code, stdout=stdout, stderr=stderr)

        except asyncio.TimeoutError:
            # Kill the process on timeout
            try:
                process.kill()
                await process.wait()
            except ProcessLookupError:
                pass  # Process already terminated

            return CommandResult(
                exit_code=124,  # Standard timeout exit code
                stdout="",
                stderr=f"Command timed out after {timeout}s",
            )

    except (OSError, ValueError) as e:
        logger.error(f"Failed to run command {cmd}: {e}")
        return CommandResult(
            exit_code=1, stdout="", stderr=f"Failed to execute command: {e}"
        )


async def run_chunked(
    base_cmd: list[str],
    files: list[str],
    chunk_size: int = 200,
    timeout: Optional[float] = None,
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
) -> list[CommandResult]:
    """
    Run a command on files in chunks to avoid command line length limits.

    Args:
        base_cmd: Base command (e.g., ["black", "--check"])
        files: List of files to process
        chunk_size: Number of files per chunk
        timeout: Timeout per chunk
        cwd: Working directory
        env: Environment variables

    Returns:
        List of CommandResult objects, one per chunk
    """
    if not files:
        return []

    results = []

    for i in range(0, len(files), chunk_size):
        chunk = files[i : i + chunk_size]
        cmd = base_cmd + chunk

        result = await run(cmd, timeout=timeout, cwd=cwd, env=env)
        results.append(result)

        # If a chunk fails badly, stop processing
        if result.exit_code > 1:  # 1 is often "issues found", >1 is usually fatal
            break

    return results


def combine_results(results: list[CommandResult]) -> CommandResult:
    """
    Combine multiple CommandResult objects into a single result.

    Args:
        results: List of results to combine

    Returns:
        Combined CommandResult
    """
    if not results:
        return CommandResult(exit_code=0, stdout="", stderr="")

    # Use the highest exit code
    exit_code = max(r.exit_code for r in results)

    # Combine all output
    stdout_parts = [r.stdout for r in results if r.stdout.strip()]
    stderr_parts = [r.stderr for r in results if r.stderr.strip()]

    stdout = "\n".join(stdout_parts)
    stderr = "\n".join(stderr_parts)

    return CommandResult(exit_code=exit_code, stdout=stdout, stderr=stderr)
