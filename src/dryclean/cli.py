"""
dryclean CLI entry point.

usage:
  dryclean init             Set up quality checks in the current repo
  dryclean run              Run all checks with auto-fix
  dryclean run --ci         Run all checks in report-only mode
  dryclean commit FILE      Validate commit message format
  dryclean check LANG NAME  Run a single check script
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from dryclean.checker import run_checks
from dryclean.constant import CLAUDE_MD_PATH, WORKFLOW_PATH
from dryclean.github import setup_github
from dryclean.hook import install_hooks, validate_commit_message
from dryclean.util import header, info, read_template, warning, write_file

_CLAUDE_MD_TEMPLATE = "CLAUDE.md.tmpl"
_SCRIPTS_ROOT = Path(__file__).parent / "scripts"
_WORKFLOW_TEMPLATE = "dryclean.yml.tmpl"


def _add_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparsers.add_parser("init", help="Set up quality checks in the current repo")
    run_parser = subparsers.add_parser("run", help="Run all checks with auto-fix")
    run_parser.add_argument("--ci", action="store_true", help="Run in report-only mode")
    commit_parser = subparsers.add_parser(
        "commit", help="Validate commit message format"
    )
    commit_parser.add_argument("message_file", type=Path, help="Commit message file")
    check_parser = subparsers.add_parser("check", help="Run a single check script")
    check_parser.add_argument(
        "language", help="Language folder (javascript, python, shell)"
    )
    check_parser.add_argument("script", help="Script name without .py extension")
    check_parser.add_argument(
        "remaining", nargs="*", help="Additional arguments and file paths"
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    _add_commands(parser.add_subparsers(dest="command"))
    return parser


def _handle_custom_check(args: argparse.Namespace) -> None:
    script_path = _SCRIPTS_ROOT / args.language / f"{args.script}.py"
    result = subprocess.run(
        [sys.executable, str(script_path), *args.remaining],
    )
    sys.exit(result.returncode)


def _handle_commit(args: argparse.Namespace) -> None:
    passed = validate_commit_message(args.message_file)
    sys.exit(0 if passed else 1)


def _handle_init(args: argparse.Namespace) -> None:
    header("dryclean Setup")
    write_file(CLAUDE_MD_PATH, read_template(_CLAUDE_MD_TEMPLATE))
    write_file(WORKFLOW_PATH, read_template(_WORKFLOW_TEMPLATE))
    install_hooks()
    if sys.stdin.isatty():
        setup_github()
    else:
        warning("Non-interactive shell. Skipping GitHub setup.")
    info("Done!")


def _handle_run(args: argparse.Namespace) -> None:
    all_passed = run_checks(Path("."), ci=args.ci)
    sys.exit(0 if all_passed else 1)


_COMMANDS = {
    "check": _handle_custom_check,
    "commit": _handle_commit,
    "init": _handle_init,
    "run": _handle_run,
}


def main() -> None:
    """Run the dryclean CLI."""
    parser = _build_parser()
    args = parser.parse_args()
    handler = _COMMANDS.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
