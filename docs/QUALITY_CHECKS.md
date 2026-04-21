# Quality Checks

- Git hooks run locally on every commit — fast feedback, skippable.
- CI runs on every push — cannot be bypassed.

---

## Checks

| Check                      | Local | CI |
|----------------------------|-------|----|
| prettier (with fix)        | ✓     | —  |
| prettier (report only)     | —     | ✓  |
| eslint                     | ✓     | ✓  |
| ruff lint (with fix)       | ✓     | —  |
| ruff format (with fix)     | ✓     | —  |
| ruff lint (report only)    | —     | ✓  |
| ruff format (report only)  | —     | ✓  |
| mypy                       | —     | ✓  |
| shellcheck                 | ✓     | ✓  |
| trailing whitespace (fix)  | ✓     | —  |
| end of file newline (fix)  | ✓     | —  |
| verify JSON syntax         | ✓     | ✓  |
| verify YAML syntax         | ✓     | ✓  |
| verify TOML syntax         | ✓     | ✓  |
| no merge conflict strings  | ✓     | ✓  |
| no direct checkins to main | ✓     | —  |
| commit message format      | ✓     | —  |
| quality scripts            | ✓     | ✓  |

---

## Bypassing git hooks

```bash
git commit --no-verify -m "emergency fix"
```
