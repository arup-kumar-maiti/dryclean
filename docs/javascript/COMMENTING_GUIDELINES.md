# Commenting Guidelines

Comment on **why**. Never on **what**.

---

## When to Comment

**Non-obvious behavior:**

```javascript
// Empty config object triggers default initialization in the loader
const config = {};
```

**External constraints:**

```javascript
// The API returns max 20 results regardless of the limit parameter
const results = await client.fetch(query, { limit: 20 });
```

**Deliberate non-obvious decisions:**

```javascript
// Sync read instead of async — this runs once at startup, not per-request
const skill = fs.readFileSync(skillPath, 'utf8');
```

**Known limitations:**

```javascript
// Only detects entries by string match on the command field.
// Will miss renamed copies — acceptable since we control the install path.
const has = hooks.some(h => h.command && h.command.includes(HOOK_NAME));
```

**Regex or complex expressions:**

```javascript
// Matches semantic version strings: major.minor.patch
const VERSION_PATTERN = /^\d+\.\d+\.\d+$/;
```

---

## When Not to Comment

**What the code does:**

```javascript
// Wrong
// read the file contents
const content = fs.readFileSync(path, 'utf8');
```

**Section dividers:**

```javascript
// Wrong
// --- Read config ---
// --- Write output ---
```

---

## Format

- Full sentences.
- Capital first letter.
- No period for single-line. Period for multi-line.
- Comment goes above the line it refers to, never inline.

```javascript
// Wrong
const backup = settings + '.bak';  // create backup path

// Right
// Backup path for rollback on failure
const backup = settings + '.bak';
```

---

## JSDoc

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
