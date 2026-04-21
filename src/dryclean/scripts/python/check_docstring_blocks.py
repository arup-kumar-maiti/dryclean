"""
Check that Python docstrings do not contain Args/Returns/Raises blocks.

usage:
  python scripts/python/check_docstring_blocks.py [FILE ...]
"""

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_BLOCK_HEADER = re.compile(
    r"^\s*(Args|Arguments|Parameters|Returns|Return|Raises|Yields|Yield|"
    r"Attributes|Example|Examples|Note|Notes|See Also)\s*:?\s*$"
)
_SPHINX_FIELD = re.compile(
    r"^\s*:(param|parameter|arg|argument|key|keyword|type|returns|return|"
    r"rtype|raises|raise|except|exception|var|ivar|cvar|vartype)\b"
)


@dataclass
class _FileResult:
    path: Path
    line: int
    name: str
    matched: str


def _find_forbidden_lines(docstring: str) -> list[str]:
    return [
        line.strip()
        for line in docstring.splitlines()
        if _BLOCK_HEADER.match(line) or _SPHINX_FIELD.match(line)
    ]


def _check_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef, path: Path
) -> list[_FileResult]:
    docstring = ast.get_docstring(node, clean=False)
    if not docstring:
        return []
    return [
        _FileResult(path=path, line=node.lineno, name=node.name, matched=match)
        for match in _find_forbidden_lines(docstring)
    ]


def _analyze_file(path: Path) -> list[_FileResult]:
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"WARNING:  syntax_error | {path} | skipping", file=sys.stderr)
        return []
    return [
        result
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        for result in _check_function(node, path)
    ]


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  docstring_block"
            f" | {violation.path}:{violation.line}"
            f" | '{violation.name}' | {violation.matched}"
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
