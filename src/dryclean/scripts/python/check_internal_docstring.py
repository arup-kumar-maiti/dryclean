"""
Check that Python internal helper functions have no docstring.

usage:
  python scripts/python/check_internal_docstring.py [FILE ...]
"""

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class _FileResult:
    path: Path
    line: int
    name: str


def _is_internal_helper(name: str) -> bool:
    return name.startswith("_") and not (name.startswith("__") and name.endswith("__"))


def _analyze_file(path: Path) -> list[_FileResult]:
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"WARNING:  syntax_error | {path} | skipping", file=sys.stderr)
        return []

    return [
        _FileResult(path=path, line=node.lineno, name=node.name)
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and _is_internal_helper(node.name)
        and ast.get_docstring(node) is not None
    ]


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  internal_docstring"
            f" | {violation.path}:{violation.line} | '{violation.name}'"
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
