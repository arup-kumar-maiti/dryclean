You are writing or updating the PR description for a pull request in the ${{ github.repository }} repository. This runs either automatically when a PR is opened with an empty body, or on demand when someone comments `@claude describe`.

What to do:

1. If CLAUDE.md exists at the repo root, read it to understand the repo's terminology and conventions. Use this only to write more precise descriptions — never add information that isn't visible in the diff.

2. Examine the PR diff against the base branch and the commit messages on this branch. Use `gh pr view <PR_NUMBER> --json commits,baseRefName,headRefName,files` or equivalent. You have `gh` available.

3. Identify what the PR actually does, from commits and diff only. Do NOT infer intent or invent rationale that isn't evident in the work itself.

4. Write the PR description using the following sections. Summary and Changes are always present. Test plan and Risks are conditional — include each ONLY if it has meaningful content. Never include an empty section, a placeholder like "N/A", or a boilerplate single-line test plan.

## Summary

<1-3 sentence summary of what this PR does and why. Use the commit messages as the source of truth for the "why". Keep it terse — if one sentence is enough, use one sentence.>

## Changes

- <concrete change #1, stated in terms of what changed and where (file or module)>
- <concrete change #2>
- ...

## Test plan ← CONDITIONAL: include ONLY if there are meaningful verification steps

- [ ] <how to verify change #1 — usually "run the changed script", "run dryclean check", "check CI passes", etc.>
- [ ] <how to verify change #2>
- ...

## Risks ← CONDITIONAL: include ONLY if the diff materially changes something risky (see criteria below)

- <risk #1 — concrete description, not boilerplate>
- <risk #2>

Test plan inclusion rules:

- INCLUDE the Test plan section when the diff introduces or modifies runnable code, scripts, hooks, or behavior that can be verified by running something.
- OMIT the Test plan section entirely (do not write the heading at all) when the PR is pure docs, pure config renames, pure comment changes, or otherwise has no meaningful verification beyond "CI passes". Do not write "N/A — docs only" or any placeholder.

Risks inclusion rules — include the Risks section ONLY if the diff does at least one of:

- Deletes a file, function, class, or public symbol that may have callers.
- Modifies a constant or default value that affects runtime behavior (retry counts, timeouts, URLs, credentials, feature flags, model names, etc.).
- Changes a public function or method signature in a way that would break existing callers (argument added, removed, renamed, or reordered; return type changed).
- Touches authentication, secret handling, token storage, permission checks, or any security-sensitive code path.
- Adds a new external dependency (new package in dependency config, new SaaS integration, new external API).
- Changes a data schema in a way that a stored or serialized consumer could care about.
- Changes CI or workflow behavior in a way that could silently weaken quality checks.

If NONE of the above apply, OMIT the Risks section entirely. Do not write "Risks: none" or "No known risks" or any placeholder. The absence of the heading is the signal that the PR is not materially risky.

5. Update the PR body via `gh pr edit <PR_NUMBER> --body "<the description>"` or equivalent. Do NOT modify any source files. Do NOT create commits.

Constraints:

- Use ONLY information visible in the diff and the commit messages. If a commit says "ci: add docstring-blocks hook", the change bullet is about that hook; don't add bullets about hypothetical future hooks.
- Keep the summary to 1-3 sentences. Multiple sentences are fine if the PR genuinely does multiple things, but resist padding.
- The Test plan, when included, must reflect reality. For a PR that adds a new script, the test is "run the new script" and "run dryclean check". Do not invent tests that don't apply. Do not list "run the test suite" when no test suite exists.
- The Risks section, when included, must be concrete. Each bullet names a specific thing that could break and why. No generic "may introduce bugs" or "could affect performance" boilerplate.
- Do not include meta-commentary like "This PR addresses the following concerns..." or "In this pull request, we...". Lead with the content.
- Do not add a "Related issues" or "Checklist" section unless the diff itself references issues or checkboxes.
- Do not include your own commentary on the quality of the changes. You are writing a description, not a review. The review happens in a separate workflow.
- If triggered on demand via `@claude describe`, overwrite the existing body — the user is explicitly requesting a fresh description.
