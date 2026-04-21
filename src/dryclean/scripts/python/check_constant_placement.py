"""
Check that Python module-level constants appear before any function or class definition.

usage:
  python scripts/python/check_constant_placement.py [FILE ...]
"""

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_UPPER_SNAKE_CASE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]+$")


@dataclass
class _FileResult:
    path: Path
    line: int
    name: str


def _is_upper_snake_case(name: str) -> bool:
    return bool(_UPPER_SNAKE_CASE_PATTERN.match(name))


def _analyze_file(path: Path) -> list[_FileResult]:
    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"WARNING:  syntax_error | {path} | skipping", file=sys.stderr)
        return []

    preamble_ended = False
    results: list[_FileResult] = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            preamble_ended = True
            continue

        if not preamble_ended:
            continue

        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if isinstance(target, ast.Name) and _is_upper_snake_case(target.id):
                results.append(_FileResult(path=path, line=node.lineno, name=target.id))

    return results


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  constant_placement | {violation.path}:{violation.line}"
            f" | '{violation.name}' must be at the top of the module"
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
