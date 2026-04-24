"""Run quality checks via pre-commit with dryclean configs."""

import os
import re
from pathlib import Path

import yaml

from dryclean.constant import DRYCLEAN_BIN, PRE_COMMIT_BIN
from dryclean.util import (
    CommandOptions,
    info,
    read_template,
    run_command,
    warning,
    write_file,
)

_CACHE_ERROR_PATTERN = re.compile(r"Executable `.+` not found|Could not find \".+\"")
_CONFIG_DIR = Path("/tmp/dryclean")
_CONFIG_FILE = "dryclean.yml"
_DRYCLEAN_ENTRY_PREFIX = "entry: dryclean "
_PRE_COMMIT_CI = "pre-commit-ci.yaml"
_PRE_COMMIT_LOCAL = "pre-commit-local.yaml"
_SKIP_ENV_VAR = "SKIP"
_SKIPPED_MARKER = "Skipped"
_TEMPLATE_NAMES = [
    "eslintrc.json",
    "htmlhintrc.json",
    "mypy.ini",
    _PRE_COMMIT_CI,
    _PRE_COMMIT_LOCAL,
    "prettierrc.json",
    "ruff.toml",
    "stylelintrc.json",
    "taplo.toml",
]


def _ensure_configs() -> None:
    _CONFIG_DIR.mkdir(exist_ok=True)
    for name in _TEMPLATE_NAMES:
        content = read_template(f"{name}.tmpl")
        content = content.replace(_DRYCLEAN_ENTRY_PREFIX, f"entry: {DRYCLEAN_BIN} ")
        write_file(_CONFIG_DIR / name, content, overwrite=True)


def _load_skip_list(directory: Path) -> list[str]:
    config_path = directory / _CONFIG_FILE
    if not config_path.exists():
        return []
    skip = (yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}).get("skip")
    return skip if isinstance(skip, list) else []


def _build_skip_env(
    directory: Path, cli_skip: list[str] | None = None
) -> dict[str, str]:
    skip_list = _load_skip_list(directory) + (cli_skip or [])
    return (
        {**os.environ, _SKIP_ENV_VAR: ",".join(skip_list)}
        if skip_list
        else dict(os.environ)
    )


def _is_stale_cache(hook_output: str) -> bool:
    return bool(_CACHE_ERROR_PATTERN.search(hook_output))


def run_checks(
    directory: Path, ci: bool = False, skip: list[str] | None = None
) -> bool:
    """Run all quality checks and skip any specified hooks."""
    _ensure_configs()
    config = _PRE_COMMIT_CI if ci else _PRE_COMMIT_LOCAL
    config_path = _CONFIG_DIR / config
    command = [PRE_COMMIT_BIN, "run", "--all-files", "--config", str(config_path)]
    options = CommandOptions(
        cwd=directory,
        env=_build_skip_env(directory, skip),
        skip_lines_containing=_SKIPPED_MARKER,
        stream=True,
    )
    try:
        result = run_command(command, options)
        if result.returncode != 0 and _is_stale_cache(result.stdout):
            info("Stale cache. Clean and retry.")
            run_command([PRE_COMMIT_BIN, "clean"], CommandOptions(silent=True))
            result = run_command(command, options)
        return result.returncode == 0
    except FileNotFoundError:
        warning("Pre-commit not found. Skipping.")
        return True
