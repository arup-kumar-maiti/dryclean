"""
Check that Python custom exception classes are only defined in exception.py.

usage:
  python scripts/python/check_exception_location.py [FILE ...]
"""

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path

_EXCEPTION_BASE_NAMES = frozenset({"Exception", "BaseException"})
_EXCEPTION_FILENAME = "exception.py"
_EXCEPTION_NAME_SUFFIXES = ("Error", "Exception")


@dataclass
class _FileResult:
    path: Path
    class_name: str


def _is_exception_class(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name):
            name = base.id
            if name in _EXCEPTION_BASE_NAMES or name.endswith(_EXCEPTION_NAME_SUFFIXES):
                return True
        if isinstance(base, ast.Attribute) and base.attr.endswith(
            _EXCEPTION_NAME_SUFFIXES
        ):
            return True
    return False


def _analyze_file(path: Path) -> list[_FileResult]:
    if path.name == _EXCEPTION_FILENAME:
        return []

    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"WARNING:  syntax_error | {path} | skipping", file=sys.stderr)
        return []

    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and _is_exception_class(node):
            violations.append(
                _FileResult(
                    path=path,
                    class_name=node.name,
                )
            )
    return violations


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  exception_location"
            f" | {violation.path} | '{violation.class_name}'"
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
