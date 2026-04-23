"""
Check that all Shell files have executable permission.

usage:
  python scripts/shell/check_executable_permission.py [FILE ...]
"""

import argparse
import os
import sys
from pathlib import Path


def _find_violations(files: list[Path]) -> list[Path]:
    return [path for path in files if not os.access(path, os.X_OK)]


def _print_report(violations: list[Path]) -> None:
    for path in violations:
        print(f"VIOLATION:  executable_permission | {path} | not executable")


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
