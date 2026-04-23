"""
Check that no Python file exceeds the max allowed comment-to-code ratio.

usage:
  python scripts/python/check_comment_density.py [--max-ratio 0.15] [FILE ...]
"""

import argparse
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

_COMMENT_PREFIX = "#"
_DEFAULT_MAX_RATIO = 0.15


@dataclass
class _FileResult:
    path: Path
    code_lines: int
    comment_lines: int

    @property
    def ratio(self) -> float:
        if self.code_lines == 0:
            return 0.0
        return self.comment_lines / self.code_lines


def _analyze_file(path: Path) -> _FileResult:
    with path.open("rb") as source:
        tokens = list(tokenize.tokenize(source.readline))

    comment_lines: set[int] = set()
    for token_type, _, start, _, _ in tokens:
        if token_type == tokenize.COMMENT:
            comment_lines.add(start[0])

    lines = path.read_text(encoding="utf-8").splitlines()
    code_lines = sum(
        1
        for line_num, line in enumerate(lines, start=1)
        if line.strip()
        and not line.strip().startswith(_COMMENT_PREFIX)
        and line_num not in comment_lines
    )

    return _FileResult(
        path=path,
        code_lines=code_lines,
        comment_lines=len(comment_lines),
    )


def _find_violations(files: list[Path], max_ratio: float) -> list[_FileResult]:
    results = [_analyze_file(path) for path in files]
    return [result for result in results if result.ratio > max_ratio]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  comment_density | {violation.path} | {violation.ratio:.1%}"
            f" comment-to-code line ratio | ({violation.comment_lines} comments /"
            f" {violation.code_lines} code lines)"
        )


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("files", nargs="*", type=Path, help="File paths to check")
    parser.add_argument(
        "--max-ratio",
        type=float,
        default=_DEFAULT_MAX_RATIO,
        help="Maximum allowed comment-to-code line ratio (default: 0.15)",
    )
    args = parser.parse_args()

    violations = _find_violations(args.files, args.max_ratio)
    _print_report(violations)
    sys.exit(0 if not violations else 1)


if __name__ == "__main__":
    main()
