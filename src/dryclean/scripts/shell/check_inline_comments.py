"""
Check that no Shell comment appears on the same line as code.

usage:
  python scripts/shell/check_inline_comments.py [FILE ...]
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_COMMENT_PREFIX = "#"
_INLINE_COMMENT = re.compile(r"^[^#'\"]*[^\s].*\s#\s")


@dataclass
class _FileResult:
    path: Path
    line: int


def _has_inline_comment(line: str) -> bool:
    return bool(_INLINE_COMMENT.search(line))


def _analyze_file(path: Path) -> list[_FileResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    results: list[_FileResult] = []

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith(_COMMENT_PREFIX):
            continue
        if _has_inline_comment(line):
            results.append(_FileResult(path=path, line=line_num))

    return results


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(f"VIOLATION:  inline_comment | {violation.path}:{violation.line}")


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
