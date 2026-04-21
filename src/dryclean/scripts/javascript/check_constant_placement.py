"""
Check that JavaScript module-level constants appear before any function definition.

usage:
  python scripts/javascript/check_constant_placement.py [FILE ...]
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_ASSIGNMENT_SEPARATOR = "="
_COMMENT_PREFIX = "//"
_CONST_KEYWORD = "const"
_CONST_PATTERN = re.compile(r"^(?:const\s+)?[A-Z][A-Z0-9_]+\s*=")
_REQUIRE_PATTERN = re.compile(r"^(?:const|let|var)\s+\w+\s*=\s*require\(")
_SHEBANG_PREFIX = "#!/"


@dataclass
class _FileResult:
    path: Path
    line: int
    name: str


def _is_preamble_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith(_SHEBANG_PREFIX):
        return True
    if stripped.startswith(_COMMENT_PREFIX):
        return True
    if _REQUIRE_PATTERN.match(stripped):
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

        if preamble_ended and _CONST_PATTERN.match(stripped):
            name = (
                stripped.split(_ASSIGNMENT_SEPARATOR)[0]
                .replace(_CONST_KEYWORD, "")
                .strip()
            )
            results.append(_FileResult(path=path, line=line_num, name=name))

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
