# Commenting Guidelines

Comment on **why**. Never on **what**.

---

## When to Comment

**Non-obvious behavior:**

```python
# Free-tier users get rate-limited after 100 requests, not blocked.
# This preserves their session state while reducing server load.
if user.tier == "free" and request_count > MAX_FREE_REQUESTS:
    apply_rate_limit(user)
```

**External constraints:**

```python
# The upstream API returns max 50 results regardless of the limit parameter.
# Paginate with offset to get full coverage.
results = client.fetch(query, limit=50, offset=page * 50)
```

**Deliberate non-obvious decisions:**

```python
# Round to nearest dollar instead of exact cents.
# Sub-dollar differences should not create separate cache entries.
cache_key = f"{category}:{rounded_price}"
```

**Known limitations:**

```python
# Assumes timezone matches the server locale.
# Will break for distributed deployments. Accepted until we add timezone param.
current_hour = datetime.now().hour
```

**Regex or complex expressions:**

```python
# Matches semantic version strings: major.minor.patch
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
```

---

## When Not to Comment

**What the code does:**

```python
# Wrong
# add the item to the list
items.append(new_item)
```

**Type information:**

```python
# Wrong
def get_users(role: str): ...  # returns a list of users

# Right
def get_users(role: str) -> list[User]: ...
```

**Section dividers:**

```python
# Wrong
# --- Fetch data ---
# --- Validate data ---
```

---

## Format

- Full sentences.
- Capital first letter.
- No period for single-line. Period for multi-line.
- Comment goes above the line it refers to, never inline.

```python
# Wrong
retries = 0  # reset the counter

# Right
# Reset before each batch to avoid cascading failures
retries = 0
```

---

## Docstrings

- Public functions: one-line docstring.
- Internal functions: no docstring.
- No parameter or return type docs — annotations cover those.

```python
# Public
def find_user(user_id: str) -> User:
    """Return the user matching the given ID."""

# Internal
def _normalize_email(email: str) -> str:
    return email.strip().lower()
```
