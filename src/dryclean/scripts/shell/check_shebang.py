"""
Check that all Shell files have a proper shebang line.

usage:
  python scripts/shell/check_shebang.py [FILE ...]
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import typer

_EXPECTED_SHEBANG = "#!/bin/bash"


@dataclass
class _FileResult:
    path: Path
    actual: str


def _analyze_file(path: Path) -> list[_FileResult]:
    first_line = path.read_text(encoding="utf-8").split("\n", maxsplit=1)[0]
    if first_line.strip() != _EXPECTED_SHEBANG:
        return [_FileResult(path=path, actual=first_line.strip())]
    return []


def _find_violations(files: list[Path]) -> list[_FileResult]:
    return [result for path in files for result in _analyze_file(path)]


def _print_report(violations: list[_FileResult]) -> None:
    for violation in violations:
        print(
            f"VIOLATION:  shebang | {violation.path}"
            f" | expected '{_EXPECTED_SHEBANG}', got '{violation.actual}'"
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
