"""
Check that all Python source files use snake_case names.

usage:
  python scripts/python/check_snake_case_filename.py [FILE ...]
"""

import re
import sys
from pathlib import Path

import typer

_SNAKE_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _is_snake_case(path: Path) -> bool:
    return bool(_SNAKE_CASE_PATTERN.match(path.stem))


def _find_violations(files: list[Path]) -> list[Path]:
    return [path for path in files if not _is_snake_case(path)]


def _print_report(violations: list[Path]) -> None:
    for path in violations:
        print(f"VIOLATION:  snake_case_filename | {path}")


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
