# Quality Checks

- Git hooks run locally on every commit — fast feedback, skippable.
- CI runs on every push — cannot be bypassed.

---

## General

- `trailing-whitespace` — remove trailing spaces from all files. `[local: fix]`
- `end-of-file-fixer` — ensure newline at EOF for all files. `[local: fix]`
- `check-merge-conflict` — detect merge conflict strings in all files. `[local + ci]`
- `no-commit-to-branch` — block direct commits to main. `[local]`

---

## JSON

- `prettier` — format JSON files. `[local: fix | ci: report]`
- `check-json` — verify JSON syntax. `[local + ci]`

---

## TOML

- `taplo-format` — format TOML files. `[local: fix | ci: report]`
- `check-toml` — verify TOML syntax. `[local + ci]`

---

## YAML

- `prettier` — format YAML files. `[local: fix | ci: report]`
- `check-yaml` — verify YAML syntax. `[local + ci]`

---

## CSS

- `prettier` — format CSS files. `[local: fix | ci: report]`
- `stylelint` — lint CSS files. `[local + ci]`
- `check-comment-density-css` — check max 15% comment-to-code ratio per file. `[local + ci]`
- `check-comment-period-css` — check comment period punctuation rule. `[local + ci]`
- `check-inline-comments-css` — reject inline comments. `[local + ci]`
- `check-kebab-case-filename-css` — check kebab-case file names. `[local + ci]`
- `check-section-dividers-css` — reject section divider comments. `[local + ci]`

---

## HTML

- `prettier` — format HTML files. `[local: fix | ci: report]`
- `htmlhint` — lint HTML files. `[local + ci]`
- `check-comment-density-html` — check max 15% comment-to-code ratio per file. `[local + ci]`
- `check-comment-period-html` — check comment period punctuation rule. `[local + ci]`
- `check-data-attribute-naming-html` — check kebab-case data attribute names. `[local + ci]`
- `check-deprecated-elements-html` — reject deprecated elements. `[local + ci]`
- `check-inline-comments-html` — reject inline comments. `[local + ci]`
- `check-kebab-case-filename-html` — check kebab-case file names. `[local + ci]`
- `check-section-dividers-html` — reject section divider comments. `[local + ci]`

---

## JavaScript

- `prettier` — format JavaScript files. `[local: fix | ci: report]`
- `eslint` — lint JavaScript files. `[local + ci]`
- `check-comment-density-js` — check max 15% comment-to-code ratio per file. `[local + ci]`
- `check-comment-period-js` — check comment period punctuation rule. `[local + ci]`
- `check-constant-placement-js` — check constants before function definitions. `[local + ci]`
- `check-function-length-js` — check max 30 lines per function. `[local + ci]`
- `check-inline-comments-js` — reject inline comments. `[local + ci]`
- `check-kebab-case-filename-js` — check kebab-case file names. `[local + ci]`
- `check-section-dividers-js` — reject section divider comments inside functions. `[local + ci]`

---

## Python

- `ruff-format` — format Python files. `[local: fix | ci: report]`
- `ruff-check` — lint Python files. `[local: fix | ci: report]`
- `mypy` — check strict type annotations. `[ci]`
- `check-argument-count-py` — check max 4 arguments per function. `[local + ci]`
- `check-comment-density-py` — check max 15% comment-to-code ratio per file. `[local + ci]`
- `check-comment-period-py` — check comment period punctuation rule. `[local + ci]`
- `check-constant-placement-py` — check constants before function or class definitions. `[local + ci]`
- `check-docstring-blocks-py` — reject Args/Returns/Raises blocks in docstrings. `[local + ci]`
- `check-exception-location-py` — check custom exceptions in exception.py only. `[local + ci]`
- `check-function-length-py` — check max 30 lines per function. `[local + ci]`
- `check-inline-comments-py` — reject inline comments. `[local + ci]`
- `check-internal-docstring-py` — reject docstrings on internal helper functions. `[local + ci]`
- `check-section-dividers-py` — reject section divider comments inside functions or methods. `[local + ci]`
- `check-snake-case-filename-py` — check snake_case file names. `[local + ci]`

---

## Shell

- `shellcheck` — lint Shell files. `[local + ci]`
- `check-comment-density-sh` — check max 15% comment-to-code ratio per file. `[local + ci]`
- `check-comment-period-sh` — check comment period punctuation rule. `[local + ci]`
- `check-executable-permission-sh` — check executable permission. `[local + ci]`
- `check-inline-comments-sh` — reject inline comments. `[local + ci]`
- `check-kebab-case-filename-sh` — check kebab-case file names. `[local + ci]`
- `check-section-dividers-sh` — reject section divider comments. `[local + ci]`
- `check-shebang-sh` — check `#!/bin/bash` shebang line. `[local + ci]`
- `check-strict-mode-sh` — check `set -e` strict error handling. `[local + ci]`

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
