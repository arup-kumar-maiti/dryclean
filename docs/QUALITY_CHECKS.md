# Quality Checks

- Git hooks run locally on every commit — fast feedback, skippable.
- CI runs on every push — cannot be bypassed.

---

## General

- `trailing-whitespace` — Remove trailing spaces from all files `[local: fix]`
- `end-of-file-fixer` — Ensure newline at EOF for all files `[local: fix]`
- `check-merge-conflict` — Detect merge conflict strings in all files `[local + ci]`
- `no-commit-to-branch` — Block direct commits to main `[local]`

---

## JSON

- `prettier` — Format JSON files `[local: fix | ci: report]`
- `check-json` — Verify JSON syntax `[local + ci]`

---

## TOML

- `taplo-format` — Format TOML files `[local: fix | ci: report]`
- `check-toml` — Verify TOML syntax `[local + ci]`

---

## YAML

- `prettier` — Format YAML files `[local: fix | ci: report]`
- `check-yaml` — Verify YAML syntax `[local + ci]`

---

## CSS

- `prettier` — Format CSS files `[local: fix | ci: report]`
- `stylelint` — Lint CSS files `[local + ci]`
- `check-comment-density-css` — Check max 15% comment-to-code ratio per file `[local + ci]`
- `check-comment-period-css` — Check comment period punctuation rule `[local + ci]`
- `check-inline-comments-css` — Reject inline comments `[local + ci]`
- `check-kebab-case-filename-css` — Check kebab-case file names `[local + ci]`
- `check-section-dividers-css` — Reject section divider comments `[local + ci]`

---

## HTML

- `prettier` — Format HTML files `[local: fix | ci: report]`
- `htmlhint` — Lint HTML files `[local + ci]`
- `check-comment-density-html` — Check max 15% comment-to-code ratio per file `[local + ci]`
- `check-comment-period-html` — Check comment period punctuation rule `[local + ci]`
- `check-data-attribute-naming-html` — Check kebab-case data attribute names `[local + ci]`
- `check-deprecated-elements-html` — Reject deprecated elements `[local + ci]`
- `check-inline-comments-html` — Reject inline comments `[local + ci]`
- `check-kebab-case-filename-html` — Check kebab-case file names `[local + ci]`
- `check-section-dividers-html` — Reject section divider comments `[local + ci]`

---

## JavaScript

- `prettier` — Format JavaScript files `[local: fix | ci: report]`
- `eslint` — Lint JavaScript files `[local + ci]`
- `check-comment-density-js` — Check max 15% comment-to-code ratio per file `[local + ci]`
- `check-comment-period-js` — Check comment period punctuation rule `[local + ci]`
- `check-constant-placement-js` — Check constants before function definitions `[local + ci]`
- `check-function-length-js` — Check max 30 lines per function `[local + ci]`
- `check-inline-comments-js` — Reject inline comments `[local + ci]`
- `check-kebab-case-filename-js` — Check kebab-case file names `[local + ci]`
- `check-section-dividers-js` — Reject section divider comments inside functions `[local + ci]`

---

## Python

- `ruff-format` — Format Python files `[local: fix | ci: report]`
- `ruff-check` — Lint Python files `[local: fix | ci: report]`
- `mypy` — Check strict type annotations `[ci]`
- `check-argument-count-py` — Check max 4 arguments per function `[local + ci]`
- `check-comment-density-py` — Check max 15% comment-to-code ratio per file `[local + ci]`
- `check-comment-period-py` — Check comment period punctuation rule `[local + ci]`
- `check-constant-placement-py` — Check constants before function or class definitions `[local + ci]`
- `check-docstring-blocks-py` — Reject Args/Returns/Raises blocks in docstrings `[local + ci]`
- `check-exception-location-py` — Check custom exceptions in exception.py only `[local + ci]`
- `check-function-length-py` — Check max 30 lines per function `[local + ci]`
- `check-inline-comments-py` — Reject inline comments `[local + ci]`
- `check-internal-docstring-py` — Reject docstrings on internal helper functions `[local + ci]`
- `check-section-dividers-py` — Reject section divider comments inside functions or methods `[local + ci]`
- `check-snake-case-filename-py` — Check snake_case file names `[local + ci]`

---

## Shell

- `shellcheck` — Lint Shell files `[local + ci]`
- `check-comment-density-sh` — Check max 15% comment-to-code ratio per file `[local + ci]`
- `check-comment-period-sh` — Check comment period punctuation rule `[local + ci]`
- `check-executable-permission-sh` — Check executable permission `[local + ci]`
- `check-inline-comments-sh` — Reject inline comments `[local + ci]`
- `check-kebab-case-filename-sh` — Check kebab-case file names `[local + ci]`
- `check-section-dividers-sh` — Reject section divider comments `[local + ci]`
- `check-shebang-sh` — Check `#!/bin/bash` shebang line `[local + ci]`
- `check-strict-mode-sh` — Check `set -e` strict error handling `[local + ci]`

---

## Skip hooks

Skip persistent hooks with a `dryclean.yml` file in the repo root.

```yaml
skip:
  - check-comment-density-py
  - stylelint
```

Skip one-off hooks with the `--skip` flag.

```bash
dryclean run --skip check-comment-density-py,stylelint
```

Use either, both, or neither. Expect a merged skip list when both are present.

---

## Bypass git hooks

```bash
git commit --no-verify -m "emergency fix"
```
