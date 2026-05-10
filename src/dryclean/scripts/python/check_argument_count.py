"""
Check that no Python function or method exceeds the max allowed argument count.

usage:
  python scripts/python/check_argument_count.py [--max-args 4] [FILE ...]
"""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

import typer

_DEFAULT_MAX_ARGS = 4


@dataclass
class _FunctionResult:
    path: Path
    function_name: str
    arg_count: int


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

        all_args = node.args.args + node.args.posonlyargs + node.args.kwonlyargs
        caller_args = [
            parameter for parameter in all_args if parameter.arg not in ("self", "cls")
        ]

        results.append(
            _FunctionResult(
                path=path,
                function_name=node.name,
                arg_count=len(caller_args),
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
