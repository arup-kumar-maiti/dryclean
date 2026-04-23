"""
Check that standalone CSS comments follow the period punctuation rule.

usage:
  python scripts/css/check_comment_period.py [FILE ...]
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_BLOCK_CLOSE = "*/"
_BLOCK_OPEN = "/*"
_DIRECTIVE_PATTERNS = re.compile(r"^\s*(?:stylelint|prettier|postcss)")
_PERIOD = "."
_SINGLE_LINE_BLOCK_SIZE = 1


@dataclass
class _FileResult:
    path: Path
    line: int
    rule: str


def _extract_comment_text(line: str) -> str:
    text = line.strip()
    if text.startswith(_BLOCK_OPEN):
        text = text[len(_BLOCK_OPEN) :]
    if text.endswith(_BLOCK_CLOSE):
        text = text[: -len(_BLOCK_CLOSE)]
    text = text.strip()
    if text.startswith("*"):
        text = text[1:].strip()
    return text


def _is_directive(comment: str) -> bool:
    return bool(_DIRECTIVE_PATTERNS.match(comment))


def _collect_comment_blocks(path: Path) -> list[list[tuple[int, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []
    in_comment = False

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not in_comment and stripped.startswith(_BLOCK_OPEN):
            text = _extract_comment_text(stripped)
            if _BLOCK_CLOSE in stripped:
                if text and not _is_directive(text):
                    blocks.append([(line_num, text)])
            else:
                in_comment = True
                if text and not _is_directive(text):
                    current = [(line_num, text)]
        elif in_comment:
            text = _extract_comment_text(stripped)
            if text:
                current.append((line_num, text))
            if _BLOCK_CLOSE in stripped:
                in_comment = False
                if current:
                    blocks.append(current)
                    current = []

    return blocks


def _ends_with_period(comment: str) -> bool:
    return comment.rstrip().endswith(_PERIOD)


def _check_block(block: list[tuple[int, str]]) -> list[tuple[int, str]]:
    if len(block) == _SINGLE_LINE_BLOCK_SIZE:
        if _ends_with_period(block[0][1]):
            return [(block[0][0], "single_line_trailing_period")]
        return []
    return [
        (line_num, "multi_line_missing_period")
        for line_num, text in block
        if not _ends_with_period(text)
    ]


def _analyze_file(path: Path) -> list[_FileResult]:
    blocks = _collect_comment_blocks(path)
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
