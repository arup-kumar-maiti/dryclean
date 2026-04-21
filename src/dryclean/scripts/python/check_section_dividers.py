"""
Check that section divider comments do not appear inside Python function bodies.

usage:
  python scripts/python/check_section_dividers.py [FILE ...]
"""

import argparse
import ast
import re
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

_DIVIDER_PATTERNS = (
    re.compile(r"^\s*step\s*\d+\b", re.IGNORECASE),
    re.compile(r"^\s*region\b", re.IGNORECASE),
    re.compile(r"^\s*endregion\b", re.IGNORECASE),
    re.compile(r"^\s*section\b", re.IGNORECASE),
    re.compile(r"^\s*\d+[.):]\s"),
)


@dataclass
class _FunctionRange:
    start: int
    end: int


@dataclass
class _FileResult:
    path: Path
    line: int


def _is_line_inside_any(line: int, ranges: list[_FunctionRange]) -> bool:
    return any(r.start <= line <= r.end for r in ranges)


def _find_comments_in_ranges(
    path: Path, ranges: list[_FunctionRange]
) -> list[tokenize.TokenInfo]:
    with path.open("rb") as source:
        tokens = list(tokenize.tokenize(source.readline))
    return [
        token
        for token in tokens
        if token.type == tokenize.COMMENT
        and _is_line_inside_any(token.start[0], ranges)
    ]


def _is_divider(comment: str) -> bool:
    body = comment.lstrip("#")
    return any(pattern.match(body) for pattern in _DIVIDER_PATTERNS)


def _analyze_file(path: Path) -> list[_FileResult]:
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"WARNING:  syntax_error | {path} | skipping", file=sys.stderr)
        return []
    ranges = [
        _FunctionRange(start=node.lineno, end=node.end_lineno or node.lineno)
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    if not ranges:
        return []
    return [
        _FileResult(path=path, line=token.start[0])
        for token in _find_comments_in_ranges(path, ranges)
        if _is_divider(token.string)
    ]


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
