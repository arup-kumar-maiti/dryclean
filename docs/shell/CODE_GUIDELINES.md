# Code Guidelines

> **CI** = fails PR automatically · **Review** = caught in code review

---

## Stack

- Bash, shellcheck

---

## Naming [CI · Review]

- Files: `kebab-case`. **[CI]**
  - Verb or verb phrase. **[Review]**
- Variables:
  - Local: `lower_snake_case`. **[Review]**
  - Exported/environment: `UPPER_SNAKE_CASE`. **[Review]**
  - Full words, no abbreviations except ones more recognizable than the full form (e.g. `api`, `db`, `id`, `ip`, `url`) — never lazy shorthand (e.g. `btn`, `cfg`, `ctx`, `err`, `msg`, `req`, `res`, `usr`). **[Review]**
- Unclear name → rename first. **[Review]**

---

## Shebangs [CI]

- `#!/bin/bash` on line 1.
- Strict mode: `set -e` in every file.

---

## Constants [Review]

- No magic strings or numbers. Use named variables.
  - In comparisons (`[ "$retries" -lt 3 ]`).
  - In defaults and variable expansion. Inline strings in error messages are fine.

---

## Error Handling [CI · Review]

- No `eval` with dynamic input. **[CI]**
- Check file/dir existence before operations. **[Review]**
- Print a descriptive error message before exiting on failure. **[Review]**
- Never swallow silently. **[Review]**

---

## Comments [CI]

- Max 15% comment-to-code ratio per file.
- What to comment and how → [Commenting Guidelines](COMMENTING_GUIDELINES.md).

---

## Formatting [CI]

- No trailing whitespace.
- Newline at end of every file.
- Executable permission on all `.sh` files.
- Quote all variable expansions (`"$VAR"`, not `$VAR`).
- `shellcheck` is final — no manual overrides.
