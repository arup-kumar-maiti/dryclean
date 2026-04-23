"""
Check that CSS files contain no ID selectors used for styling.

usage:
  python scripts/css/check_no_id_selectors.py [FILE ...]
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_BLOCK_CLOSE = "*/"
_BLOCK_OPEN = "/*"
# Matches # followed by a letter, underscore, or hyphen (ID selector).
# Does not match # followed by hex digits only (color value).
_ID_SELECTOR_PATTERN = re.compile(r"#[a-zA-Z_-]")
_PROPERTY_VALUE_PATTERN = re.compile(r"^\s*[\w-]+\s*:")


@dataclass
class _FileResult:
    path: Path
    line: int


def _is_property_line(line: str) -> bool:
    return bool(_PROPERTY_VALUE_PATTERN.match(line))


def _analyze_file(path: Path) -> list[_FileResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    results: list[_FileResult] = []
    in_comment = False

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        if in_comment:
            if _BLOCK_CLOSE in stripped:
                in_comment = False
            continue

        if stripped.startswith(_BLOCK_OPEN):
            if _BLOCK_CLOSE not in stripped:
                in_comment = True
            continue

        if _is_property_line(stripped):
            continue

        if _ID_SELECTOR_PATTERN.search(stripped):
            results.append(_FileResult(path=path, line=line_num))

    return results


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(f"VIOLATION:  no_id_selector | {violation.path}:{violation.line}")


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
