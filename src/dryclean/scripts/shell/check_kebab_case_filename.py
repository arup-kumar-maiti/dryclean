"""
Check that all Shell source files use kebab-case names.

usage:
  python scripts/shell/check_kebab_case_filename.py [FILE ...]
"""

import argparse
import re
import sys
from pathlib import Path

_KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z]+$")


def _is_kebab_case(path: Path) -> bool:
    return bool(_KEBAB_CASE_PATTERN.match(path.name))


def _find_violations(files: list[Path]) -> list[Path]:
    return [path for path in files if not _is_kebab_case(path)]


def _print_report(violations: list[Path]) -> None:
    for path in violations:
        print(f"VIOLATION:  kebab_case_filename | {path}")


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
