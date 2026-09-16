from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

###定义统一的 ExecutionResult 结果格式

@dataclass(slots=True)
class ExecutionResult:
    """The stable result contract returned by Harness v0."""

    command: list[str]
    repo_path: str
    passed: bool
    return_code: int | None
    duration_seconds: float
    stdout: str
    stderr: str
    error_type: str | None = None
    timed_out: bool = False
    result_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert the result to JSON-compatible data."""
        return asdict(self)
