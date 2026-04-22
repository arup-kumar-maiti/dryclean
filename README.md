# dryclean

Multi-language code quality toolkit. One install. Every JavaScript, Python, and Shell file — checked.

## Quick Start

```bash
pip install dryclean
dryclean init
```

`dryclean init` — Write `CLAUDE.md`, the CI workflow, and git hooks. In an interactive shell, also prompt to configure GitHub branch protection and store a Claude Code OAuth token.

## Commands

```bash
# Set up quality checks in the current repo
dryclean init
# Run all checks with auto-fix
dryclean run
# Run all checks in report-only mode
dryclean run --ci
```

## What Gets Checked

| Language   | Formatter | Linter     | Type Checker |
|------------|-----------|------------|--------------|
| JavaScript | prettier  | eslint     | —            |
| Python     | ruff      | ruff       | mypy         |
| Shell      | —         | shellcheck | —            |

Plus: trailing whitespace, EOF newlines, JSON/YAML/TOML syntax, merge conflicts, no direct commits to main, commit message format, and 25 custom quality scripts.

## GitHub Actions

```yaml
- uses: arup-kumar-maiti/dryclean/ci@v1

- uses: arup-kumar-maiti/dryclean/review@v1
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}

- uses: arup-kumar-maiti/dryclean/describe@v1
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

## Supported Languages

- JavaScript (.js)
- Python (.py)
- Shell (.sh)
