![CI](https://github.com/arup-kumar-maiti/dryclean/actions/workflows/dryclean.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![PyPI](https://img.shields.io/pypi/v/dryclean)
![Downloads](https://img.shields.io/pypi/dm/dryclean)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)

# dryclean

Multi-language code quality toolkit. One install. Check every supported file.

## Prerequisites

- Python 3.11+
- Node.js 18+ (for CSS, HTML, and JavaScript support)

## Quickstart

```bash
pip install dryclean
dryclean init
```

`dryclean init` — write `CLAUDE.md`, the CI workflow, and git hooks. In an interactive shell, also configure GitHub branch protection and store a Claude Code OAuth token.

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

Refer to [Quality Checks](https://github.com/arup-kumar-maiti/dryclean/blob/main/docs/QUALITY_CHECKS.md) for hook IDs, skip configuration, and supported languages.

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

## Show Your Support

Add the badge to your project's README:

```markdown
[![checked with: dryclean](https://img.shields.io/badge/checked%20with-dryclean-purple)](https://github.com/arup-kumar-maiti/dryclean)
```
