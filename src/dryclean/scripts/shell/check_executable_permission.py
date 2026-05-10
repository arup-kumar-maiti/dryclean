"""
Check that all Shell files have executable permission.

usage:
  python scripts/shell/check_executable_permission.py [FILE ...]
"""

import os
import sys
from pathlib import Path

import typer


def _find_violations(files: list[Path]) -> list[Path]:
    return [path for path in files if not os.access(path, os.X_OK)]


def _print_report(violations: list[Path]) -> None:
    for path in violations:
        print(f"VIOLATION:  executable_permission | {path} | not executable")


def _run(
    files: list[Path] = typer.Argument(default=None),
) -> None:
    violations = _find_violations(files or [])
    _print_report(violations)
    sys.exit(0 if not violations else 1)


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    typer.run(_run)


if __name__ == "__main__":
    main()
