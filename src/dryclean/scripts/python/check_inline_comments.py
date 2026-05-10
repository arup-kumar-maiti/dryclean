"""
Check that no Python comment appears on the same line as code.

usage:
  python scripts/python/check_inline_comments.py [FILE ...]
"""

import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

import typer

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


def _has_inline_comment(tokens: list[tokenize.TokenInfo], comment_index: int) -> bool:
    comment_line = tokens[comment_index].start[0]
    for prior in reversed(tokens[:comment_index]):
        if prior.start[0] != comment_line:
            return False
        if prior.type not in _WHITESPACE_TOKEN_TYPES:
            return True
    return False


def _analyze_file(path: Path) -> list[_FileResult]:
    with path.open("rb") as source:
        tokens = list(tokenize.tokenize(source.readline))

    return [
        _FileResult(path=path, line=token.start[0])
        for index, token in enumerate(tokens)
        if token.type == tokenize.COMMENT and _has_inline_comment(tokens, index)
    ]


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(f"VIOLATION:  inline_comment | {violation.path}:{violation.line}")


def _run(
    files: list[Path] = typer.Argument(default=None),
) -> None:
    violations = _find_violations(files or [])
    _print_report(violations)
    sys.exit(0 if not violations else 1)


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    typer.run(_run)


if __name__ == "__main__":
    main()
