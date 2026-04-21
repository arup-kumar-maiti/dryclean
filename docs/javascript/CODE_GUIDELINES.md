# Code Guidelines

> **CI** = fails PR automatically · **Review** = caught in code review

---

## Stack

- Node.js, Prettier, ESLint

---

## Naming [CI · Review]

- Files: `kebab-case`. **[CI]**
  - Components/modules: singular noun. **[Review]**
  - Scripts/CLIs: verb or verb phrase. **[Review]**
- Variables: `camelCase`. **[CI]**
  - Full words, no abbreviations except ones more recognizable than the full form (e.g. `api`, `db`, `id`, `ip`, `url`) or external API field names — never lazy shorthand (e.g. `btn`, `cfg`, `ctx`, `err`, `msg`, `req`, `res`, `usr`). **[Review]**
- Constants: `UPPER_SNAKE_CASE`. **[Review]**
- Functions: `camelCase`. **[CI]**
  - Verb or verb phrase. **[Review]**
- Unclear name → rename first. **[Review]**

---

## Imports [CI]

- Order: built-in → third-party → internal, each group separated by a blank line.
- `require` only, no ESM `import`.
- No duplicate imports.
- No unused imports.

---

## Constants [CI · Review]

- No magic numbers or strings. Use named constants.
  - In comparisons (`if (x === 3)`). **[CI]**
  - In defaults and template literals. Inline strings in error messages are fine. **[Review]**
- Local constants → module top. **[CI]**

---

## Functions [CI · Review]

- Max 4 arguments. **[CI]**
- 5+ arguments → use an options object. **[Review]**
- Max 30 lines. **[CI]**
- One responsibility. **[Review]**
- Never return `undefined` and a value from the same function. **[CI]**

---

## Error Handling [CI · Review]

- No empty `catch` blocks without re-throwing or logging. **[CI]**
- Throw specific errors. **[Review]**
- Never swallow silently. **[Review]**

---

## Output [CI]

- `process.stdout.write` / `process.stderr.write`, not `console.log`.

---

## Comments [CI]

- Max 15% comment-to-code ratio per file.
- What to comment and how → [Commenting Guidelines](COMMENTING_GUIDELINES.md).

---

## Formatting [CI]

- No trailing whitespace.
- Newline at end of every file.
- Single quotes.
- `prettier` formats, `eslint` lints — no manual overrides.
