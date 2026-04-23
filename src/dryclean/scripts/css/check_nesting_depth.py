"""
Check that CSS files do not exceed the maximum nesting depth.

usage:
  python scripts/css/check_nesting_depth.py [--max-depth 3] [FILE ...]
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

_BLOCK_CLOSE = "*/"
_BLOCK_OPEN = "/*"
_BRACE_CLOSE = "}"
_BRACE_OPEN = "{"
_DEFAULT_MAX_DEPTH = 3


@dataclass
class _FileResult:
    path: Path
    line: int
    depth: int


def _analyze_file(path: Path, max_depth: int) -> list[_FileResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    results: list[_FileResult] = []
    in_comment = False
    depth = 0

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

        for char in stripped:
            if char == _BRACE_OPEN:
                depth += 1
                if depth > max_depth:
                    results.append(_FileResult(path=path, line=line_num, depth=depth))
            elif char == _BRACE_CLOSE:
                depth = max(0, depth - 1)

    return results


def _find_violations(files: list[Path], max_depth: int) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path, max_depth)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  nesting_depth | {violation.path}:{violation.line}"
            f" | nesting depth {violation.depth} exceeds maximum"
        )


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("files", nargs="*", type=Path, help="File paths to check")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=_DEFAULT_MAX_DEPTH,
        help="Maximum allowed nesting depth (default: 3)",
    )
    args = parser.parse_args()

    violations = _find_violations(args.files, args.max_depth)
    _print_report(violations)
    sys.exit(0 if not violations else 1)


if __name__ == "__main__":
    main()
