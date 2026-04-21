# Commenting Guidelines

Comment on **why**. Never on **what**.

---

## When to Comment

**Non-obvious behavior:**

```bash
# Config file may not exist on first run — create with empty object
[ ! -f "$CONFIG_FILE" ] && echo '{}' > "$CONFIG_FILE"
```

**External constraints:**

```bash
# The deploy script expects this exact directory structure
mkdir -p "$DEPLOY_DIR/bin" "$DEPLOY_DIR/config"
```

**Deliberate non-obvious decisions:**

```bash
# Backup before modifying — user may have custom settings we must not lose
cp "$CONFIG_FILE" "$CONFIG_FILE.bak"
```

**Known limitations:**

```bash
# Only detects entries by string match on the name field.
# Will miss renamed copies — acceptable since we control the install path.
has=$(grep -q "$HOOK_NAME" "$CONFIG_FILE")
```

**Regex or complex expressions:**

```bash
# Matches semantic version strings: major.minor.patch
if echo "$version" | grep -qE "^[0-9]+\.[0-9]+\.[0-9]+$"; then
```

---

## When Not to Comment

**What the code does:**

```bash
# Wrong
# copy the file to the target directory
cp "$SOURCE" "$TARGET"
```

**Section dividers:**

```bash
# Wrong
# --- Copy files ---
# --- Set permissions ---
```

---

## Format

- Full sentences.
- Capital first letter.
- No period for single-line. Period for multi-line.
- Comment goes above the line it refers to, never inline.

```bash
# Wrong
cp "$CONFIG" "$CONFIG.bak"  # backup first

# Right
# Backup before modifying user config
cp "$CONFIG" "$CONFIG.bak"
```
