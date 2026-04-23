"""
Check that all Shell files use set -e for strict error handling.

usage:
  python scripts/shell/check_strict_mode.py [FILE ...]
"""

import argparse
import sys
from pathlib import Path

_STRICT_MODE = "set -e"


def _find_violations(files: list[Path]) -> list[Path]:
    return [
        path for path in files if _STRICT_MODE not in path.read_text(encoding="utf-8")
    ]


def _print_report(violations: list[Path]) -> None:
    for path in violations:
        print(f"VIOLATION:  strict_mode | {path} | missing 'set -e'")


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
