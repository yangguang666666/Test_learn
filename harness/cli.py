from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .artifacts import save_result
from .runner import run_pytest

###命令行入口

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Harness v0: run pytest and save a structured result."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository directory to test. Defaults to the current directory.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Maximum test duration in seconds. Defaults to 60.",
    )
    parser.add_argument(
        "--result",
        default="artifacts/harness_result.json",
        help="JSON output path. Defaults to artifacts/harness_result.json.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    # Test output can contain Chinese text while PowerShell uses a legacy code page.
    # Replace unsupported characters instead of crashing after the subprocess ends.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    args, pytest_args = build_parser().parse_known_args(argv)
    if pytest_args and pytest_args[0] == "--":
        pytest_args.pop(0)

    result = run_pytest(
        Path(args.repo),
        timeout_seconds=args.timeout,
        pytest_args=pytest_args,
    )
    output_path = save_result(result, args.result)

    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    print(f"Saved result to: {output_path}")
    return 0 if result.passed else 1
