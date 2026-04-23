# Code Guidelines

> **CI** = fails PR automatically · **Review** = caught in code review

---

## Stack

- Python 3.11+, Pydantic, ruff, mypy (strict)

---

## Naming [CI · Review]

- Files: `snake_case`. **[CI]**
  - Singular noun. **[Review]**
- Variables: `snake_case`. **[CI]**
- Constants: `UPPER_SNAKE_CASE`. **[CI]**
- Classes: `PascalCase`. **[CI]**
  - Noun or noun phrase. **[Review]**
- Functions: `snake_case`. **[CI]**
  - Verb or verb phrase. **[Review]**
- Full words, no abbreviations except ones more recognizable than the full form (e.g. `api`, `db`, `id`, `ip`, `url`) or external API field names — never lazy shorthand (e.g. `btn`, `cfg`, `ctx`, `err`, `msg`, `req`, `res`, `usr`). **[Review]**
- Unclear name → rename first. **[Review]**

---

## Imports [CI]

- Order: stdlib → third-party → internal, each group separated by a blank line.
- No wildcard imports.
- No duplicate imports.
- No unused imports.

---

## Constants [CI · Review]

- No magic numbers or strings. Use config or named constants.
  - In comparisons (`if x == 3`). **[Review]**
  - In defaults and format strings. Inline f-strings in `raise` are fine. **[Review]**
- Local constants → module top. **[CI]**
- Shared constants → `constant.py`. **[Review]**

---

## Types [CI · Review]

- Function signatures: always annotated. **[CI]**
- API, service, config data: Pydantic models. **[Review]**
- Internal data: dataclasses. **[Review]**

---

## Functions [CI · Review]

- Return type: always annotated. **[CI]**
- Max 4 arguments. **[CI]**
- 5+ arguments → use a dataclass or Pydantic model. **[Review]**
- Max 30 lines. **[CI]**
- One responsibility. **[Review]**
- Never return `None` and a value from the same function. **[Review]**

---

## Error Handling [CI · Review]

- No bare `except:` or `except Exception:` without re-raising or logging. **[CI]**
- Custom exceptions → `exception.py`. **[CI]**
- Raise specific exceptions. **[Review]**
- Never swallow silently. **[Review]**

---

## Comments [CI]

- Max 15% comment-to-code ratio per file.
- What to comment and how → [Commenting Guidelines](COMMENTING_GUIDELINES.md).

---

## Formatting [CI]

- No trailing whitespace.
- Newline at end of every file.
- One blank line between methods in a class.
- Two blank lines between top-level definitions.
- Double quotes.
- `ruff` is final — no manual overrides.
