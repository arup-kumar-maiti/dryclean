"""Install git hooks and validate commit messages."""

import sys
from pathlib import Path

from dryclean.constant import COMMITIZEN_BIN
from dryclean.util import error, run_command, warning

_ALLOWED_PREFIXES = ["ci", "docs", "feat", "fix", "init", "refactor", "test"]
_HOOK_PERMISSION = 0o755
_HOOKS_DIR = Path(".git/hooks")

_TEMPLATE_COMMIT_HOOK = """#!/bin/bash
set -e
"{python}" -m dryclean.cli commit "$1"
"""

_TEMPLATE_LOCAL_HOOK = """#!/bin/bash
set -e
"{python}" -m dryclean.cli run
"""


def install_hooks() -> None:
    """Write dryclean hooks into .git/hooks/."""
    if not _HOOKS_DIR.exists():
        error("Not a git repository.")
        sys.exit(1)

    python_path = sys.executable

    pre_commit_path = _HOOKS_DIR / "pre-commit"
    pre_commit_path.write_text(
        _TEMPLATE_LOCAL_HOOK.format(python=python_path),
        encoding="utf-8",
    )
    pre_commit_path.chmod(_HOOK_PERMISSION)

    commit_msg_path = _HOOKS_DIR / "commit-msg"
    commit_msg_path.write_text(
        _TEMPLATE_COMMIT_HOOK.format(python=python_path),
        encoding="utf-8",
    )
    commit_msg_path.chmod(_HOOK_PERMISSION)


def validate_commit_message(message_file: Path) -> bool:
    """Validate the commit message using commitizen."""
    try:
        return (
            run_command(
                [
                    COMMITIZEN_BIN,
                    "check",
                    "--commit-msg-file",
                    str(message_file),
                    "--allowed-prefixes",
                    *_ALLOWED_PREFIXES,
                ]
            ).returncode
            == 0
        )
    except FileNotFoundError:
        warning("Commitizen not found. Skipping.")
        return True
