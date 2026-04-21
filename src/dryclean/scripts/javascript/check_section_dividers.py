"""
Check that section divider comments do not appear inside JavaScript functions.

usage:
  python scripts/javascript/check_section_dividers.py [FILE ...]
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_COMMENT_PREFIX = "//"
_DIVIDER_PATTERNS = (
    re.compile(r"^\s*step\s*\d+\b", re.IGNORECASE),
    re.compile(r"^\s*region\b", re.IGNORECASE),
    re.compile(r"^\s*endregion\b", re.IGNORECASE),
    re.compile(r"^\s*section\b", re.IGNORECASE),
    re.compile(r"^\s*\d+[.):]\s"),
)
_FUNCTION_PATTERN = re.compile(
    r"(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>|\w+\s*=>))"
)


@dataclass
class _FunctionRange:
    start: int
    end: int


@dataclass
class _FileResult:
    path: Path
    line: int


def _find_function_ranges(lines: list[str]) -> list[_FunctionRange]:
    ranges: list[_FunctionRange] = []
    in_function = False
    function_start = 0
    brace_depth = 0

    for i, line in enumerate(lines):
        if _FUNCTION_PATTERN.search(line) and not in_function:
            function_start = i + 1
            in_function = True
            brace_depth = 0

        if in_function:
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0 and "}" in line:
                ranges.append(_FunctionRange(start=function_start, end=i + 1))
                in_function = False

    return ranges


def _is_divider(comment_body: str) -> bool:
    return any(pattern.match(comment_body) for pattern in _DIVIDER_PATTERNS)


def _analyze_file(path: Path) -> list[_FileResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    ranges = _find_function_ranges(lines)
    if not ranges:
        return []

    results: list[_FileResult] = []
    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith(_COMMENT_PREFIX):
            continue
        comment_body = stripped[len(_COMMENT_PREFIX) :]
        if not any(r.start <= line_num <= r.end for r in ranges):
            continue
        if _is_divider(comment_body):
            results.append(_FileResult(path=path, line=line_num))

    return results


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(f"VIOLATION:  section_divider | {violation.path}:{violation.line}")


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
