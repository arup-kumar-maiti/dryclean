"""Shared constants."""

import sys
from pathlib import Path

_BIN_DIR = Path(sys.executable).parent

CLAUDE_MD_PATH = Path("CLAUDE.md")
COMMITIZEN_BIN = str(_BIN_DIR / "cz")
DRYCLEAN_BIN = str(_BIN_DIR / "dryclean")
PRE_COMMIT_BIN = str(_BIN_DIR / "pre-commit")
TEMPLATES_ROOT = Path(__file__).parent / "templates"
WORKFLOW_PATH = Path(".github/workflows/dryclean.yml")
