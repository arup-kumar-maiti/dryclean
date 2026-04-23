"""
Check that standalone Python comments follow the period punctuation rule.

usage:
  python scripts/python/check_comment_period.py [FILE ...]
"""

import argparse
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

_DIRECTIVE_PREFIXES = (
    "!",
    " -*-",
    " noqa",
    " type:",
    " pragma:",
    " pylint:",
    " mypy:",
    " fmt:",
    " isort:",
)
_PERIOD = "."
_SINGLE_LINE_BLOCK_SIZE = 1
_WHITESPACE_TOKEN_TYPES = frozenset(
    {
        tokenize.NL,
        tokenize.NEWLINE,
        tokenize.INDENT,
        tokenize.DEDENT,
        tokenize.ENCODING,
    }
)


@dataclass
class _FileResult:
    path: Path
    line: int
    rule: str


def _is_directive(comment: str) -> bool:
    return comment[1:].startswith(_DIRECTIVE_PREFIXES)


def _collect_standalone_comments(path: Path) -> list[tokenize.TokenInfo]:
    with path.open("rb") as source:
        tokens = list(tokenize.tokenize(source.readline))

    standalone: list[tokenize.TokenInfo] = []
    code_lines: set[int] = set()
    for token in tokens:
        line = token.start[0]
        if token.type == tokenize.COMMENT:
            if line not in code_lines and not _is_directive(token.string):
                standalone.append(token)
        elif token.type not in _WHITESPACE_TOKEN_TYPES:
            code_lines.add(line)
    return standalone


def _continues_block(
    previous_token: tokenize.TokenInfo, current_token: tokenize.TokenInfo
) -> bool:
    return (
        previous_token.start[0] + 1 == current_token.start[0]
        and previous_token.start[1] == current_token.start[1]
    )


def _group_into_blocks(
    comments: list[tokenize.TokenInfo],
) -> list[list[tokenize.TokenInfo]]:
    blocks: list[list[tokenize.TokenInfo]] = []
    current: list[tokenize.TokenInfo] = []
    for comment in comments:
        if current and _continues_block(current[-1], comment):
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


def _check_block(block: list[tokenize.TokenInfo]) -> list[tuple[int, str]]:
    if len(block) == _SINGLE_LINE_BLOCK_SIZE:
        if _ends_with_period(block[0].string):
            return [(block[0].start[0], "single_line_trailing_period")]
        return []
    return [
        (token.start[0], "multi_line_missing_period")
        for token in block
        if not _ends_with_period(token.string)
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
