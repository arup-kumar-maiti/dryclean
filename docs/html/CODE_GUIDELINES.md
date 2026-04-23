# Code Guidelines

> **CI** = fails PR automatically · **Review** = caught in code review

---

## Stack

- Prettier, HTMLHint

---

## Naming [CI · Review]

- Files: `kebab-case`. **[CI]**
  - Singular noun. **[Review]**
- Data attributes: `data-kebab-case`. **[CI]**
- Full words, no abbreviations except ones more recognizable than the full form (e.g. `id`, `img`, `nav`, `url`) — never lazy shorthand (e.g. `btn`, `desc`, `hdr`, `usr`). **[Review]**
- Unclear name → rename first. **[Review]**

---

## Elements [CI · Review]

- Semantic elements over generic `<div>` and `<span>`. **[Review]**
- No deprecated elements. **[CI]**
- Alt text on all `<img>` elements. **[CI]**
- No inline styles. **[CI]**
- No inline event handlers. **[CI]**

---

## Comments [CI]

- Max 15% comment-to-code ratio per file.
- What to comment and how → [Commenting Guidelines](COMMENTING_GUIDELINES.md).

---

## Formatting [CI]

- No trailing whitespace.
- Newline at end of every file.
- Boolean attributes: no value (`disabled`, not `disabled="true"`).
- Double quotes.
- `prettier` formats, `htmlhint` lints — no manual overrides.
