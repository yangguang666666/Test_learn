from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Mapping, Sequence

from .models import ExecutionResult

###执行命令、捕获输出、超时处理和基础错误分类

def _text(value: str | bytes | None) -> str:
    """Normalize subprocess output for JSON and terminal display."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def classify_failure(stdout: str, stderr: str, return_code: int | None) -> str | None:
    """Classify common failures without trying to diagnose their root cause."""
    if return_code in (None, 0):
        return None

    output = f"{stdout}\n{stderr}"
    if return_code == 5 or "no tests collected" in output:
        return "NoTestsCollected"
    markers = (
        ("SyntaxError", "SyntaxError"),
        ("ModuleNotFoundError", "ModuleNotFoundError"),
        ("ImportError", "ImportError"),
        ("AssertionError", "AssertionError"),
        ("NoTestsCollected", "no tests ran"),
    )
    for error_type, marker in markers:
        if marker in output:
            return error_type
    return "TestFailure"


def run_command(
    repo_path: str | Path,
    command: Sequence[str],
    *,
    timeout_seconds: float = 60.0,
    env: Mapping[str, str] | None = None,
) -> ExecutionResult:
    """Run one command in a repository and capture its complete result."""
    repo = Path(repo_path).expanduser().resolve()
    if not repo.is_dir():
        raise NotADirectoryError(f"Repository path does not exist: {repo}")

    command_list = [str(part) for part in command]
    if not command_list:
        raise ValueError("command must contain at least one item")

    process_env = os.environ.copy()
    if env:
        process_env.update({str(key): str(value) for key, value in env.items()})

    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command_list,
            cwd=repo,
            env=process_env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - started
        stdout = _text(exc.stdout)
        stderr = _text(exc.stderr)
        return ExecutionResult(
            command=command_list,
            repo_path=str(repo),
            passed=False,
            return_code=None,
            duration_seconds=round(duration, 3),
            stdout=stdout,
            stderr=stderr,
            error_type="TimeoutExpired",
            timed_out=True,
        )

    duration = time.perf_counter() - started
    stdout = _text(completed.stdout)
    stderr = _text(completed.stderr)
    return ExecutionResult(
        command=command_list,
        repo_path=str(repo),
        passed=completed.returncode == 0,
        return_code=completed.returncode,
        duration_seconds=round(duration, 3),
        stdout=stdout,
        stderr=stderr,
        error_type=classify_failure(stdout, stderr, completed.returncode),
    )


def run_pytest(
    repo_path: str | Path,
    *,
    timeout_seconds: float = 60.0,
    pytest_args: Sequence[str] | None = None,
) -> ExecutionResult:
    """Run pytest with the same Python interpreter that runs Harness."""
    command = [sys.executable, "-m", "pytest"]
    command.extend(str(arg) for arg in (pytest_args or []))
    return run_command(
        repo_path,
        command,
        timeout_seconds=timeout_seconds,
    )
