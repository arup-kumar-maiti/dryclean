# CLAUDE.md

Non-negotiable rules for this repo. Language-specific details are in `docs/<language>/CODE_GUIDELINES.md` and `docs/<language>/COMMENTING_GUIDELINES.md`.

- `[CI]` — build fails automatically. No way to merge a violation.
- `[Review]` — self-enforce first. Caught by the automated Claude PR reviewer and human review as backup.
- `[CI · Review]` — mixed section: each bullet inside carries its own per-rule tag.

---

## Quick reference

| Convention        | CSS                  | JavaScript           | Python             | Shell                          |
|-------------------|----------------------|----------------------|--------------------|--------------------------------|
| File naming       | `kebab-case`         | `kebab-case`         | `snake_case`       | `kebab-case`                   |
| Variable naming   | —                    | `camelCase`          | `snake_case`       | `lower_snake` / `UPPER_SNAKE`  |
| Function naming   | —                    | `camelCase`          | `snake_case`       | —                              |
| Constant naming   | —                    | `UPPER_SNAKE_CASE`   | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE`             |
| Class naming      | `kebab-case`         | —                    | `PascalCase`       | —                              |
| Custom properties | `--kebab-case`       | —                    | —                  | —                              |
| Quotes            | Double               | Single               | Double             | —                              |
| Imports           | —                    | built-in → 3rd → int | stdlib → 3rd → int | —                              |
| Formatter         | prettier             | prettier             | ruff               | —                              |
| Linter            | stylelint            | eslint               | ruff               | shellcheck                     |
| Type checker      | —                    | —                    | mypy (strict)      | —                              |
| Docstrings        | —                    | JSDoc                | Docstrings         | —                              |

---

## Universal rules (all languages)

### Pre-edit checklist

Before writing or modifying any source file:

- [ ] Filename follows the language convention (see quick reference)
- [ ] Every function: ≤ 30 lines, ≤ 4 args, one responsibility
- [ ] No magic numbers / strings — extract to a module-top constant
- [ ] Imports grouped with one blank line between groups
- [ ] Comments only for *why*, on the line **above**, never inline, ≤ 15% density
- [ ] No trailing whitespace, newline at EOF
- [ ] All non-code text follows Tone rules
- [ ] Ordering follows Ordering rules

### Naming `[CI · Review]`

- Full words — abbreviations only if more recognizable than the full form (e.g. `api`, `db`, `id`, `ip`, `url`), never lazy shorthand (e.g. `btn`, `cfg`, `ctx`, `err`, `msg`, `req`, `res`, `usr`). External API field names are fine if documented with a comment. `[Review]`
- Unclear name? **Rename first, before doing anything else.** `[Review]`

### Constants `[CI · Review]`

- No magic numbers or strings anywhere. Extract every literal to a named constant. `[Review]`
  - In comparisons. `[Review]`
  - In defaults and format strings. Inline strings in error messages are fine. `[Review]`
- **Local** to one module → top of that module. `[CI]`

### Functions `[CI · Review]`

- **≤ 4 arguments.** `[CI]`
- **≤ 30 lines.** `[CI]`
- **One responsibility per function.** `[Review]`
- **Never return both `None`/`undefined` and a value** from the same function. `[Review]` (`[CI]` in JS via `consistent-return`)

### Error handling `[Review]`

- Raise / throw **specific** errors, not generic `Exception` or `Error`.
- Never swallow silently.
- Language-specific CI rules are in each language section below.

### Tone `[Review]`

All non-code text uses **imperative voice, present tense**. No gerunds, no passive, no third-person.

- Docstrings → imperative verb, one sentence, trailing period → `Return the contents of a template file.`, not `Returns the contents…` or `Gets the contents…`.
- Names and labels (e.g. workflow steps, action descriptions, CLI help) → imperative verb + object, no period → `Run quality checks`, not `Runs quality checks` or `Running quality checks`.
- User-facing messages (error, info, warning) → full sentence, sentence case, trailing period → `Pre-commit not found. Skipping.`, not `pre-commit not found`.
- Changelog entries under Added / Removed → noun phrase, no verb → `CLI with init and run commands.`, not `Add CLI with…`.
- Changelog entries under Fixed / Changed → imperative verb → `Restrict trigger to semver tags.`, not `Trigger restricted to…`.
- No filler, no hedging ("might", "could", "please"), no meta-commentary ("This will…", "Let's…").

### Comment rules `[CI · Review]`

**Comment on _why_. Never on _what_.** `[Review]`

Comment ONLY for one of these five reasons:
1. Non-obvious behavior
2. External constraints / API quirks
3. Deliberate non-obvious decisions / tradeoffs
4. Known limitations accepted for now
5. Regex or genuinely complex expressions

NEVER comment to:
- Restate what the code does `[Review]`
- Restate type information `[Review]`
- Add section dividers `[CI]`

Comment format:
- Full sentences, capital first letter. `[Review]`
- Single-line: no trailing period. Multi-line: period on each line. `[CI]`
- Comment goes on the line **above** the code. **Never inline.** `[CI]`
- Max 15% comment-to-code ratio per file. `[CI]`

### Formatting `[CI]`

- No trailing whitespace.
- Newline at end of every file.
- The language linter is the source of truth — **never** hand-tweak its output.

### Ordering `[Review]`

**Alphabetical** unless a stronger ordering exists:

- Config and declaration keys → alphabetical.
- Lists with no natural order → alphabetical.
- Imports have their own rule (see language sections) — that takes precedence.

**Code guidelines** (sections, bullets, sub-bullets) → natural reading order, not alphabetical. Order by what you encounter or do first when reading or writing a file.

```
Sections: Stack → Naming → Imports → Constants → … → Comments → Formatting
```

**Functions in a module** → callees before callers (leaf-first), grouped by call chain:

```
_parse()             ← called by validate
validate()           ← called by main (1st)
_format()            ← called by render
render()             ← called by main (2nd)
main()               ← entry point, always last
```

### Git

- **Never commit to `main`.** Branch first.
- Commit prefix: `ci`, `docs`, `feat`, `fix`, `init`, `refactor`, `test`.
- `git commit --no-verify` exists for emergencies but **CI re-runs every check**. Don't use it to dodge a real failure.

### Changelog `[Review]`

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Update `CHANGELOG.md` before every version tag.

- Categories in this order: **Added**, **Changed**, **Removed**, **Fixed** — include only what applies.
- Entry tone rules are in the Tone section above.

---

## CSS rules

Apply these when editing `.css` files, in addition to universal rules.

### Anti-patterns — DON'T

- Deep nesting (> 3 levels) → flatten selectors.
- ID selectors for styling → use class selectors.
- Magic numbers (`padding: 37px`) → use custom properties.
- Qualified selectors (`div.class`) → use class alone.
- Using `!important` → fix specificity instead.

### Naming `[CI · Review]`

- Files: `kebab-case`, singular noun. `[Review]`
- Classes: `kebab-case`. `[CI]`
- Custom properties: `--kebab-case`. `[CI]`

### Custom properties `[CI · Review]`

- Local → narrowest applicable scope. `[Review]`
- Shared → `:root`. `[Review]`

### Selectors `[CI · Review]`

- Prefer class selectors over element selectors. `[Review]`
- No ID selectors for styling — use classes instead. `[CI]`
- No qualified selectors unless specificity requires it. `[CI]`
- Max 3 levels of nesting. `[CI]`
- No `!important` — fix specificity instead. `[CI]`

### Formatting `[CI]`

- One declaration per line.
- **Double quotes**.
- `prettier` formats, `stylelint` lints — no manual overrides.

---

## JavaScript rules

Apply these when editing `.js` files, in addition to universal rules.

### Anti-patterns — DON'T

- Adding a 5th parameter → wrap in an options object.
- Double quotes (`"foo"`) → always single.
- Empty `catch` blocks → re-throw or log.
- Returning `undefined` from one branch and a value from another → pick one shape.
- Using `console.log` → use `process.stdout.write` / `process.stderr.write`.
- Using ESM `import` → use `require` (CommonJS).

### Naming `[CI · Review]`

- Files: `kebab-case`. Components: singular noun. Scripts: verb phrase. `[Review]`
- Variables: `camelCase`. `[CI]`
- Constants: `UPPER_SNAKE_CASE`. `[Review]`
- Functions: `camelCase`, verb or verb phrase. `[Review]`

### Imports `[CI]`

- Order: **built-in → third-party → internal**.
- `require` only, no ESM `import`.
- No duplicate imports. No unused imports.

### Constants `[CI · Review]`

- In comparisons. `[CI]`

### Functions `[CI · Review]`

- 5+ args → use an **options object**. `[Review]`

### Error handling `[CI · Review]`

- No empty `catch` blocks without re-throwing or logging. `[CI]`

### Output `[CI]`

- `process.stdout.write` / `process.stderr.write`, not `console.log`.

### Formatting `[CI]`

- **Single quotes** for all strings.
- `prettier` formats, `eslint` lints — no manual overrides.

### JSDoc `[Review]`

- Public functions: one-line JSDoc.
- Internal functions: no JSDoc.

```javascript
// Public
/** Return the parsed config from the given file path. */
function readConfig(configPath) {
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

// Internal
function buildDefaultConfig() {
  return { version: 1, enabled: true };
}
```

---

## Python rules

Apply these when editing `.py` files, in addition to universal rules.

### Anti-patterns — DON'T

- `# noqa` / `# type: ignore` → fix the code, don't suppress.
- Adding `Args:` / `Returns:` / `Raises:` blocks to docstrings → annotations cover it.
- Adding a 5th parameter → wrap in a dataclass / Pydantic model.
- Defining a custom exception outside `exception.py` → all exceptions live there.
- `from foo import *` or unused imports → both fail CI.
- Returning `User | None` from one branch and `User` from another → pick one shape.
- Single quotes (`'foo'`) → always double.
- Splitting a long function with `# region` / `# step 1` → extract real helpers.
- `try: ... except Exception: pass` → raise specific, don't swallow.

### Naming `[CI · Review]`

- Files: `snake_case`, singular noun. `[Review]`
- Variables: `snake_case`. `[CI]`
- Constants: `UPPER_SNAKE_CASE`. `[CI]`
- Classes: `PascalCase`, noun or noun phrase. `[Review]`
- Functions: `snake_case`, verb or verb phrase. `[Review]`

### Imports `[CI]`

- Order: **stdlib → third-party → internal**.
- No wildcard imports. No duplicate imports. No unused imports.

### Constants `[CI · Review]`

- Shared constants → `constant.py`. `[Review]`

### Types `[CI · Review]`

- Every function signature fully annotated, **including return type**. `[CI]`
- Boundary data (API / service / config) → **Pydantic model**. `[Review]`
- Internal data structures → **dataclass**. `[Review]`
- `mypy --strict` must pass. `[CI]`

### Functions `[CI · Review]`

- Return type **always annotated**. `[CI]`
- 5+ args → wrap in a **dataclass or Pydantic model**. `[Review]`

```python
# Wrong: 5 args
def send_email(recipient, subject, body, cc, priority):
    ...

# Right: model
@dataclass
class EmailRequest:
    recipient: str
    subject: str
    body: str
    cc: str
    priority: int

def send_email(request: EmailRequest) -> bool:
    ...
```

### Error handling `[CI · Review]`

- No bare `except:` / `except Exception:` unless you re-raise or log. `[CI]`
- **Every custom exception class** lives in `exception.py`. `[CI]`

```python
# Wrong
try:
    response = client.get(url)
except Exception:
    return None

# Right
try:
    response = client.get(url)
except TimeoutError as exc:
    raise ServiceTimeout(url) from exc
```

### Formatting `[CI]`

- **One** blank line between methods inside a class.
- **Two** blank lines between top-level definitions.
- **Double quotes** for all strings.
- `ruff format` is final.

### Docstrings `[CI · Review]`

- **Public functions** → exactly **one line**. `[Review]`
- **Internal helpers** (`_` prefix) → **no docstring at all**. `[CI]`
- **No `Args:`, `Returns:`, `Raises:` blocks. Ever.** `[CI]`

```python
# Public
def find_user(user_id: str) -> User:
    """Return the user matching the given ID."""

# Internal
def _normalize_email(email: str) -> str:
    return email.strip().lower()
```

---

## Shell rules

Apply these when editing `.sh` files, in addition to universal rules.

### Anti-patterns — DON'T

- Missing `set -e` → every shell file must fail on first error.
- Missing executable permission → `.sh` files must have `+x`.
- Silent `exit 1` without a message → print what went wrong first.
- Unquoted variable expansions (`$VAR` instead of `"$VAR"`) → word splitting bugs.
- Using `eval` with dynamic input → command injection risk.

### Naming `[CI · Review]`

- Files: `kebab-case`, verb or verb phrase. `[Review]`
- Local variables: `lower_snake_case`. `[Review]`
- Exported/environment variables: `UPPER_SNAKE_CASE`. `[Review]`

### Shebangs `[CI]`

- `#!/bin/bash` on line 1.
- `set -e` immediately after.

### Constants `[Review]`

- No magic numbers or strings. Use named variables.

### Error handling `[CI · Review]`

- No `eval` with dynamic input. `[CI]`
- Check file/dir existence before operations. `[Review]`
- Print a descriptive error message before exiting on failure. `[Review]`

### Formatting `[CI]`

- Executable permission on all `.sh` files.
- Quote all variable expansions (`"$VAR"`, not `$VAR`).
- `shellcheck` is final.
