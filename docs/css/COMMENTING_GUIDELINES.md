# Commenting Guidelines

Comment on **why**. Never on **what**.

---

## When to Comment

**Non-obvious behavior:**

```css
/* Negative margin offsets the parent container padding */
.card-image {
  margin-left: -1rem;
  margin-right: -1rem;
}
```

**External constraints:**

```css
/* Safari requires -webkit prefix for sticky positioning on table elements */
.table-header {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
}
```

**Deliberate non-obvious decisions:**

```css
/* Fixed height instead of min-height to prevent layout shift on load */
.hero {
  height: var(--hero-height);
}
```

**Known limitations:**

```css
/* Gap property not supported in older Safari flexbox.
   Margin fallback acceptable until minimum browser version bumps. */
.grid {
  gap: var(--spacing-md);
}
```

**Regex or complex expressions:**

```css
/* Targets every third item starting from the second */
.list-item:nth-child(3n + 2) {
  margin-top: var(--spacing-lg);
}
```

---

## When Not to Comment

**What the code does:**

```css
/* Wrong */
/* set the background color to blue */
.header {
  background-color: var(--color-primary);
}
```

**Section dividers:**

```css
/* Wrong */
/* --- Header styles --- */
/* --- Footer styles --- */
```

---

## Format

- Full sentences.
- Capital first letter.
- No period for single-line. Period for multi-line.
- Comment goes above the line it refers to, never inline.

```css
/* Wrong */
.sidebar {
  width: var(--sidebar-width); /* sidebar needs fixed width */
}

/* Right */
/* Fixed width prevents reflow when content length varies */
.sidebar {
  width: var(--sidebar-width);
}
```
