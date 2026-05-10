"""
Check that no Go function exceeds the max allowed argument count.

usage:
  python scripts/go/check_argument_count.py [--max-args 4] [FILE ...]
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import typer

_DEFAULT_MAX_ARGS = 4
_FUNC_PATTERN = re.compile(
    r"^func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(([^)]*)\)", re.MULTILINE
)


@dataclass
class _FunctionResult:
    path: Path
    function_name: str
    arg_count: int


def _count_parameters(param_string: str) -> int:
    stripped = param_string.strip()
    if not stripped:
        return 0
    return len(stripped.split(","))


def _analyze_file(path: Path) -> list[_FunctionResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    source = "\n".join(lines)
    results: list[_FunctionResult] = []

    for match in _FUNC_PATTERN.finditer(source):
        function_name = match.group(1)
        param_string = match.group(2)
        arg_count = _count_parameters(param_string)

        results.append(
            _FunctionResult(
                path=path,
                function_name=function_name,
                arg_count=arg_count,
            )
        )

    return results


def _find_violations(files: list[Path], max_args: int) -> list[_FunctionResult]:
    results = [result for path in files for result in _analyze_file(path)]
    return [result for result in results if result.arg_count > max_args]


def _print_report(violations: list[_FunctionResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  argument_count | {violation.path}:"
            f" | '{violation.function_name}' has {violation.arg_count} arguments"
        )


def _run(
    files: list[Path] = typer.Argument(default=None),
    max_args: int = typer.Option(
        _DEFAULT_MAX_ARGS, help="Maximum allowed arguments per function"
    ),
) -> None:
    violations = _find_violations(files or [], max_args)
    _print_report(violations)
    sys.exit(0 if not violations else 1)


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    typer.run(_run)


if __name__ == "__main__":
    main()
