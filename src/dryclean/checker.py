"""Run quality checks via pre-commit with dryclean configs."""

import shutil
from pathlib import Path

from dryclean.constant import TEMPLATES_ROOT
from dryclean.util import CommandOptions, run_command, warning

_CONFIG_DIR = Path("/tmp/dryclean")
_PRE_COMMIT_CI = "pre-commit-ci.yaml"
_PRE_COMMIT_LOCAL = "pre-commit-local.yaml"
_TEMPLATE_NAMES = [
    "eslintrc.json",
    "mypy.ini",
    _PRE_COMMIT_CI,
    _PRE_COMMIT_LOCAL,
    "prettierrc.json",
    "ruff.toml",
    "taplo.toml",
]


def _ensure_configs() -> None:
    _CONFIG_DIR.mkdir(exist_ok=True)
    for name in _TEMPLATE_NAMES:
        shutil.copy(TEMPLATES_ROOT / f"{name}.tmpl", _CONFIG_DIR / name)


def run_checks(directory: Path, ci: bool = False) -> bool:
    """Run all quality checks."""
    _ensure_configs()
    config = _PRE_COMMIT_CI if ci else _PRE_COMMIT_LOCAL
    config_path = _CONFIG_DIR / config
    try:
        result = run_command(
            ["pre-commit", "run", "--all-files", "--config", str(config_path)],
            CommandOptions(cwd=directory, stream=True),
        )
        return result.returncode == 0
    except FileNotFoundError:
        warning("Pre-commit not found. Skipping.")
        return True
