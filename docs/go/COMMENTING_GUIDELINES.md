# Commenting Guidelines

Comment on **why**. Never on **what**.

---

## When to Comment

**Non-obvious behavior:**

```go
// Free-tier users get rate-limited after 100 requests, not blocked.
// This preserves their session state while reducing server load.
if user.Tier == "free" && requestCount > maxFreeRequests {
    applyRateLimit(user)
}
```

**External constraints:**

```go
// The upstream API returns max 50 results regardless of the limit parameter.
// Paginate with offset to get full coverage.
results, err := client.Fetch(query, 50, page*50)
```

**Deliberate non-obvious decisions:**

```go
// Round to nearest dollar instead of exact cents.
// Sub-dollar differences should not create separate cache entries.
cacheKey := fmt.Sprintf("%s:%d", category, roundedPrice)
```

**Known limitations:**

```go
// Assumes timezone matches the server locale.
// Will break for distributed deployments. Accepted until we add timezone param.
currentHour := time.Now().Hour()
```

**Regex or complex expressions:**

```go
// Matches semantic version strings: major.minor.patch
var versionPattern = regexp.MustCompile(`^\d+\.\d+\.\d+$`)
```

---

## When Not to Comment

**What the code does:**

```go
// Wrong
// add the item to the list
items = append(items, newItem)
```

**Type information:**

```go
// Wrong
func getUsers(role string) []User { // returns a list of users

// Right
func getUsers(role string) []User {
```

**Section dividers:**

```go
// Wrong
// --- Fetch data ---
// --- Validate data ---
```

---

## Format

- Full sentences.
- Capital first letter.
- No period for single-line. Period for multi-line.
- Comment goes above the line it refers to, never inline.

```go
// Wrong
retries := 0 // reset the counter

// Right
// Reset before each batch to avoid cascading failures
retries := 0
```

---

## GoDoc

- Public functions: one-line GoDoc starting with the function name.
- Internal functions: no GoDoc.
- No parameter or return type docs — signatures cover those.

```go
// Public
// FindUser returns the user matching the given ID.
func FindUser(userID string) (User, error) {

// Internal
func normalizeEmail(email string) string {
    return strings.TrimSpace(strings.ToLower(email))
```
