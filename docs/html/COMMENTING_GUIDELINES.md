# Commenting Guidelines

Comment on **why**. Never on **what**.

---

## When to Comment

**Non-obvious behavior:**

```html
<!-- Empty action submits to the current URL for progressive enhancement -->
<form action="" method="post">
```

**External constraints:**

```html
<!-- Analytics provider requires this script in the head before DOMContentLoaded -->
<script async src="/analytics.js"></script>
```

**Deliberate non-obvious decisions:**

```html
<!-- Inline SVG instead of img tag for CSS fill control -->
<svg aria-label="Logo">
  <use href="/icons.svg#logo"></use>
</svg>
```

**Known limitations:**

```html
<!-- Safari does not support the dialog element natively.
     Polyfill loaded conditionally in the script bundle. -->
<dialog id="confirm-modal">
  ...
</dialog>
```

**Regex or complex expressions:**

```html
<!-- Matches email addresses with company domain only -->
<input type="email" pattern="[a-z]+@company\.com">
```

---

## When Not to Comment

**What the code does:**

```html
<!-- Wrong -->
<!-- unordered list of links -->
<ul>
  <li><a href="/about">About</a></li>
</ul>
```

**Section dividers:**

```html
<!-- Wrong -->
<!-- --- Header --- -->
<!-- --- Main content --- -->
```

---

## Format

- Full sentences.
- Capital first letter.
- No period for single-line. Period for multi-line.
- Comment goes above the line it refers to, never inline.

```html
<!-- Wrong -->
<a href="/about">About</a> <!-- link to about page -->

<!-- Right -->
<!-- Skip link targets the main content landmark for keyboard users -->
<a href="#main" class="skip-link">Skip to content</a>
```
