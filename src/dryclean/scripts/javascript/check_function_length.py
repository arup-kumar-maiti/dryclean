"""
Check that no JavaScript function exceeds the max allowed line count.

usage:
  python scripts/javascript/check_function_length.py [--max-lines 30] [FILE ...]
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import typer

_DEFAULT_MAX_LINES = 30
_FUNCTION_PATTERN = re.compile(
    r"(?:function\s+(\w+)"
    r"|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>|\w+\s*=>))"
)


@dataclass
class _FunctionResult:
    path: Path
    function_name: str
    line_count: int


def _analyze_file(path: Path) -> list[_FunctionResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    results: list[_FunctionResult] = []
    in_function = False
    function_start = 0
    function_name = ""
    brace_depth = 0

    for i, line in enumerate(lines):
        match = _FUNCTION_PATTERN.search(line)
        if match and not in_function:
            function_name = match.group(1) or match.group(2)
            function_start = i + 1
            in_function = True
            brace_depth = 0

        if in_function:
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0 and "}" in line:
                line_count = (i + 1) - function_start + 1
                results.append(
                    _FunctionResult(
                        path=path,
                        function_name=function_name,
                        line_count=line_count,
                    )
                )
                in_function = False

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
