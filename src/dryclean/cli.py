"""Define the dryclean CLI entry point."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer

from dryclean.checker import run_checks
from dryclean.constant import CLAUDE_MD_PATH, WORKFLOW_PATH
from dryclean.github import setup_github
from dryclean.hook import install_hooks, validate_commit_message
from dryclean.util import header, info, read_template, warning, write_file

_CLAUDE_MD_TEMPLATE = "CLAUDE.md.tmpl"
_SCRIPTS_ROOT = Path(__file__).parent / "scripts"
_WORKFLOW_TEMPLATE = "dryclean.yml.tmpl"

cli = typer.Typer(help="Multi-language code quality toolkit")


@cli.command()
def init() -> None:
    """Set up quality checks in the current repo."""
    header("dryclean Setup")
    write_file(CLAUDE_MD_PATH, read_template(_CLAUDE_MD_TEMPLATE))
    write_file(WORKFLOW_PATH, read_template(_WORKFLOW_TEMPLATE))
    install_hooks()
    if sys.stdin.isatty():
        setup_github()
    else:
        warning("Non-interactive shell. Skipping GitHub setup.")
    info("Done!")


@cli.command()
def run(
    ci: bool = typer.Option(False, help="Run in report-only mode"),
    skip: str | None = typer.Option(None, help="Skip comma-separated hook IDs"),
) -> None:
    """Run all checks with auto-fix."""
    skip_list = skip.split(",") if skip else None
    all_passed = run_checks(Path("."), ci=ci, skip=skip_list)
    sys.exit(0 if all_passed else 1)


@cli.command(hidden=True)
def commit(message_file: Path = typer.Argument(...)) -> None:
    """Validate a commit message file."""
    passed = validate_commit_message(message_file)
    sys.exit(0 if passed else 1)


@cli.command(hidden=True)
def check(
    language: str = typer.Argument(...),
    script: str = typer.Argument(...),
    remaining: list[str] | None = typer.Argument(None),
) -> None:
    """Run a language-specific check script."""
    script_path = _SCRIPTS_ROOT / language / f"{script}.py"
    result = subprocess.run(
        [sys.executable, str(script_path), *(remaining or [])],
    )
    sys.exit(result.returncode)


def main() -> None:
    """Run the dryclean CLI."""
    cli()


if __name__ == "__main__":
    main()
