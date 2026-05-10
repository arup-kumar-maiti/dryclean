"""
Check that Go package-level constants appear before any function definition.

usage:
  python scripts/go/check_constant_placement.py [FILE ...]
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import typer

_COMMENT_PREFIX = "//"
_CONST_PATTERN = re.compile(r"^const\s+(\w+)")
_FUNC_PATTERN = re.compile(r"^func\s+")
_IMPORT_PATTERN = re.compile(r"^import\s+")
_PACKAGE_PATTERN = re.compile(r"^package\s+")


@dataclass
class _FileResult:
    path: Path
    line: int
    name: str


def _is_preamble_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith(_COMMENT_PREFIX):
        return True
    if _PACKAGE_PATTERN.match(stripped):
        return True
    if _IMPORT_PATTERN.match(stripped):
        return True
    return bool(_CONST_PATTERN.match(stripped))


def _analyze_file(path: Path) -> list[_FileResult]:
    lines = path.read_text(encoding="utf-8").splitlines()
    preamble_ended = False
    results: list[_FileResult] = []

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue

        if not preamble_ended and not _is_preamble_line(line):
            preamble_ended = True

        match = _CONST_PATTERN.match(stripped)
        if preamble_ended and match:
            results.append(_FileResult(path=path, line=line_num, name=match.group(1)))

    return results


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  constant_placement | {violation.path}:{violation.line}"
            f" | '{violation.name}' must be at the top of the file"
        )


def _run(
    files: list[Path] = typer.Argument(default=None),
) -> None:
    violations = _find_violations(files or [])
    _print_report(violations)
    sys.exit(0 if not violations else 1)


def main() -> None:
    """Run the check and exit with a non-zero status if violations are found."""
    typer.run(_run)


if __name__ == "__main__":
    main()
