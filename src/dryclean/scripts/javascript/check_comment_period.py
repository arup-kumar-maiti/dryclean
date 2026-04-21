"""
Check that standalone JavaScript comments follow the period punctuation rule.

usage:
  python scripts/javascript/check_comment_period.py [FILE ...]
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_COMMENT_PREFIX = "//"
_DIRECTIVE_PATTERNS = re.compile(r"^\s*(?:eslint|noqa|type:|pragma:|fmt:|isort:)")
_PERIOD = "."
_SINGLE_LINE_BLOCK_SIZE = 1


@dataclass
class _FileResult:
    path: Path
    line: int
    rule: str


def _is_directive(comment: str) -> bool:
    return bool(_DIRECTIVE_PATTERNS.match(comment))


def _collect_standalone_comments(path: Path) -> list[tuple[int, int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    comments: list[tuple[int, int, str]] = []

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())

        if stripped.startswith(_COMMENT_PREFIX):
            comment = stripped[len(_COMMENT_PREFIX) :]
            if not _is_directive(comment):
                comments.append((line_num, indent, comment))

    return comments


def _continues_block(
    previous_line: int, previous_indent: int, current_line: int, current_indent: int
) -> bool:
    return previous_line + 1 == current_line and previous_indent == current_indent


def _group_into_blocks(
    comments: list[tuple[int, int, str]],
) -> list[list[tuple[int, int, str]]]:
    blocks: list[list[tuple[int, int, str]]] = []
    current: list[tuple[int, int, str]] = []
    for comment in comments:
        if current and _continues_block(
            current[-1][0], current[-1][1], comment[0], comment[1]
        ):
            current.append(comment)
            continue
        if current:
            blocks.append(current)
        current = [comment]
    if current:
        blocks.append(current)
    return blocks


def _ends_with_period(comment: str) -> bool:
    return comment.rstrip().endswith(_PERIOD)


def _check_block(block: list[tuple[int, int, str]]) -> list[tuple[int, str]]:
    if len(block) == _SINGLE_LINE_BLOCK_SIZE:
        if _ends_with_period(block[0][2]):
            return [(block[0][0], "single_line_trailing_period")]
        return []
    return [
        (comment[0], "multi_line_missing_period")
        for comment in block
        if not _ends_with_period(comment[2])
    ]


def _analyze_file(path: Path) -> list[_FileResult]:
    standalone = _collect_standalone_comments(path)
    blocks = _group_into_blocks(standalone)
    return [
        _FileResult(path=path, line=line, rule=rule)
        for block in blocks
        for line, rule in _check_block(block)
    ]


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  comment_period"
            f" | {violation.path}:{violation.line} | {violation.rule}"
        )


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
