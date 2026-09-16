from __future__ import annotations

import json
from pathlib import Path

from .models import ExecutionResult

###把结果保存成 UTF-8 JSON

def save_result(result: ExecutionResult, output_path: str | Path) -> Path:
    """Write one execution result as UTF-8 JSON and return its absolute path."""
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    result.result_path = str(path)
    path.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
