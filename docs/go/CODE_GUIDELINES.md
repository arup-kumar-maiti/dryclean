# Code Guidelines

> **CI** = fails PR automatically · **Review** = caught in code review

---

## Stack

- Go 1.26+, golangci-lint

---

## Naming [CI · Review]

- Files: `snake_case`. **[CI]**
  - Singular noun. **[Review]**
- Variables: `camelCase` / `PascalCase`. **[CI]**
- Constants: `camelCase` / `PascalCase`. **[CI]**
- Structs: `PascalCase`. **[CI]**
  - Noun or noun phrase. **[Review]**
- Interfaces: `PascalCase`, `-er` suffix for single-method. **[CI]**
- Functions: `camelCase` / `PascalCase`. **[CI]**
  - Verb or verb phrase. **[Review]**
- Packages: `lowercase`, single word, no underscores. **[CI]**
- Full words, no abbreviations except ones more recognizable than the full form (e.g. `api`, `db`, `id`, `ip`, `url`) or external API field names — never lazy shorthand (e.g. `btn`, `cfg`, `msg`, `req`, `res`, `usr`). **[Review]**
- Unclear name → rename first. **[Review]**

---

## Imports [CI]

- Order: stdlib → third-party → internal, each group separated by a blank line.
- No dot imports (`. "pkg"`).

---

## Constants [CI · Review]

- No magic numbers or strings. Use named constants.
  - In comparisons (`if x == 3`). **[Review]**
  - In format strings. Inline strings in error messages are fine. **[Review]**
- Local constants → file top. **[CI]**

---

## Types [Review]

- API, service, config data: structs with JSON tags.
- Internal data: structs.

---

## Functions [CI · Review]

- Max 4 arguments. **[CI]**
- 5+ arguments → use an options struct. **[Review]**
- Max 30 lines. **[CI]**
- One responsibility. **[Review]**
- Never return an error and a valid value from the same function. **[Review]**

---

## Error Handling [CI · Review]

- Return `error` as the last return value. **[CI]**
- Check every returned error — never discard with `_`. **[CI]**
- Wrap errors with `fmt.Errorf("context: %w", err)`. **[CI]**
- Never swallow silently. **[Review]**

---

## Comments [CI]

- Max 15% comment-to-code ratio per file.
- What to comment and how → [Commenting Guidelines](COMMENTING_GUIDELINES.md).

---

## Formatting [CI]

- No trailing whitespace.
- Newline at end of every file.
- One blank line between top-level definitions.
- Tabs for indentation.
- `golangci-lint` is final — no manual overrides.
