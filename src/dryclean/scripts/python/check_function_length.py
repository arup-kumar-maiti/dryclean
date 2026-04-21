"""
Check that no Python function or method exceeds the max allowed line count.

usage:
  python scripts/python/check_function_length.py [--max-lines 30] [FILE ...]
"""

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path

_DEFAULT_MAX_LINES = 30


@dataclass
class _FunctionResult:
    path: Path
    function_name: str
    line_count: int


def _analyze_file(path: Path) -> list[_FunctionResult]:
    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"WARNING:  syntax_error | {path} | skipping", file=sys.stderr)
        return []

    results = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.end_lineno is None:
            continue

        results.append(
            _FunctionResult(
                path=path,
                function_name=node.name,
                line_count=node.end_lineno - node.lineno + 1,
            )
        )

    return results


def _find_violations(files: list[Path], max_lines: int) -> list[_FunctionResult]:
    results = [result for path in files for result in _analyze_file(path)]
    return [result for result in results if result.line_count > max_lines]


def _print_report(violations: list[_FunctionResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  function_length | {violation.path}"
            f" | '{violation.function_name}' is {violation.line_count} lines"
        )


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("files", nargs="*", type=Path, help="File paths to check")
    parser.add_argument(
        "--max-lines",
        type=int,
        default=_DEFAULT_MAX_LINES,
        help="Maximum allowed lines per function (default: 30)",
    )
    args = parser.parse_args()

    violations = _find_violations(args.files, args.max_lines)
    _print_report(violations)
    sys.exit(0 if not violations else 1)


if __name__ == "__main__":
    main()
