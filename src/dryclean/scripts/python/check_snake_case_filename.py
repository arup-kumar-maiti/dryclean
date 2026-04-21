"""
Check that all Python source files use snake_case names.

usage:
  python scripts/python/check_snake_case_filename.py [FILE ...]
"""

import argparse
import re
import sys
from pathlib import Path

_SNAKE_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _is_snake_case(path: Path) -> bool:
    return bool(_SNAKE_CASE_PATTERN.match(path.stem))


def _find_violations(files: list[Path]) -> list[Path]:
    return [path for path in files if not _is_snake_case(path)]


def _print_report(violations: list[Path]) -> None:
    for path in violations:
        print(f"VIOLATION:  snake_case_filename | {path}")


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("files", nargs="*", type=Path, help="File paths to check")
    args = parser.parse_args()

    violations = _find_violations(args.files)
    _print_report(violations)
    sys.exit(0 if not violations else 1)


if __name__ == "__main__":
    main()
