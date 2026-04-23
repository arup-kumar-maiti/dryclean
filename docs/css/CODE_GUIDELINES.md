# Code Guidelines

> **CI** = fails PR automatically · **Review** = caught in code review

---

## Stack

- Prettier, Stylelint

---

## Naming [CI · Review]

- Files: `kebab-case`. **[CI]**
  - Singular noun. **[Review]**
- Classes: `kebab-case`. **[Review]**
- Custom properties: `--kebab-case`. **[Review]**
- Full words, no abbreviations except ones more recognizable than the full form (e.g. `bg`, `sm`, `md`, `lg`) — never lazy shorthand (e.g. `btn`, `clr`, `hdr`, `nav-pd`). **[Review]**
- Unclear name → rename first. **[Review]**

---

## Custom Properties [CI · Review]

- No magic numbers or strings. Use custom properties.
  - In repeated values (colors, spacing, font sizes). **[CI]**
  - In media query breakpoints. **[Review]**
- Local custom properties → narrowest applicable scope. **[Review]**
- Shared custom properties → `:root`. **[Review]**

---

## Selectors [Review]

- Prefer class selectors over element selectors.
- No ID selectors for styling — use classes instead.
- No qualified selectors (`div.class`) unless specificity requires it.
- Max 3 levels of nesting.
- No `!important` — fix specificity instead.

---

## Comments [CI]

- Max 15% comment-to-code ratio per file.
- What to comment and how → [Commenting Guidelines](COMMENTING_GUIDELINES.md).

---

## Formatting [CI]

- No trailing whitespace.
- Newline at end of every file.
- One declaration per line.
- Double quotes.
- `prettier` formats, `stylelint` lints — no manual overrides.
