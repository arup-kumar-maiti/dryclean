"""
Check that no Go function exceeds the max allowed line count.

usage:
  python scripts/go/check_function_length.py [--max-lines 30] [FILE ...]
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import typer

_DEFAULT_MAX_LINES = 30
_FUNC_PATTERN = re.compile(r"^func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(")


@dataclass
class _FunctionResult:
    path: Path
    function_name: str
    line_count: int


def _find_functions(lines: list[str]) -> list[tuple[str, int, int]]:
    functions: list[tuple[str, int, int]] = []
    in_function = False
    function_start = 0
    function_name = ""
    brace_depth = 0

    for i, line in enumerate(lines):
        match = _FUNC_PATTERN.match(line.strip())
        if match and not in_function:
            function_name = match.group(1)
            function_start = i + 1
            in_function = True
            brace_depth = 0

        if in_function:
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0 and "}" in line:
                functions.append((function_name, function_start, i + 1))
                in_function = False

    return functions


def _analyze_file(path: Path) -> list[_FunctionResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [
        _FunctionResult(path=path, function_name=name, line_count=end - start + 1)
        for name, start, end in _find_functions(lines)
    ]


def _find_violations(files: list[Path], max_lines: int) -> list[_FunctionResult]:
    results = [result for path in files for result in _analyze_file(path)]
    return [result for result in results if result.line_count > max_lines]


def _print_report(violations: list[_FunctionResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  function_length | {violation.path}"
            f" | '{violation.function_name}' is {violation.line_count} lines"
        )


def _run(
    files: list[Path] = typer.Argument(default=None),
    max_lines: int = typer.Option(
        _DEFAULT_MAX_LINES, help="Maximum allowed lines per function"
    ),
) -> None:
    violations = _find_violations(files or [], max_lines)
    _print_report(violations)
    sys.exit(0 if not violations else 1)


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    typer.run(_run)


if __name__ == "__main__":
    main()
