# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-04-24

### Added

- `dryclean.yml` config file for persistent hook skipping.
- Output filter in `run_command` for streamed line filtering.
- Quality checks documentation with hook IDs, descriptions, and skip instructions.
- `--skip` CLI flag for one-off hook skipping.

### Changed

- Add language suffix to all hook IDs for consistency.
- Reorder pre-commit hooks to run formatters before linters.
- Replace language table and supported languages list in README with link to quality checks documentation.

## [1.2.1] - 2026-04-23

### Added

- Output filter to hide skipped hooks from pre-commit terminal output.
- Streamed line filter capability in run_command utility.

## [1.2.0] - 2026-04-23

### Added

- HTML column in CLAUDE.md quick reference table and HTML rules section.
- HTML in PR review prompt language detection.
- HTML language support with code and commenting guidelines.
- HTML quality check scripts (comment density, comment period, data attribute naming, deprecated elements, inline comments, kebab-case filename, section dividers).
- HTMLHint config with rules for alt text, double quotes, inline scripts, and inline styles.
- HTMLHint integration with Prettier for HTML formatting and linting.
- JavaScript Constants section in CLAUDE.md for CI comparison override.
- Shell section dividers check script.

### Changed

- Add explicit CI and Review tags to all bullets in mixed CLAUDE.md sections.
- Add inline error message exception to universal Constants rule.
- Downgrade universal and Python magic numbers comparison tag from CI to Review.
- Replace third-party mirror repos with local node hooks for Stylelint and HTMLHint.

### Fixed

- Fix naming and docstring inconsistencies across all check scripts.

## [1.1.0] - 2026-04-23

### Added

- Code guidelines natural reading order rule in CLAUDE.md ordering section.
- CSS column in CLAUDE.md quick reference table and CSS rules section.
- CSS in PR review prompt language detection.
- CSS language support with code and commenting guidelines.
- CSS quality check scripts (comment density, comment period, inline comments, kebab-case filename, section dividers).
- Stylelint config with rules for class naming, custom property naming, declaration importance, nesting depth, ID selectors, qualified selectors, and strict value enforcement.
- Stylelint integration with Prettier for CSS formatting and linting.

### Changed

- Align CLAUDE.md section header tags with code guidelines across all languages.
- Extend Prettier to format CSS files.
- Promote universal naming rules to top-level bullets in all language code guidelines.
- Sort anti-patterns alphabetically for all languages in CLAUDE.md.

## [1.0.5] - 2026-04-22

### Fixed

- Remove pip cache from CI action to support repos without requirements.txt or pyproject.toml.

## [1.0.4] - 2026-04-21

### Added

- CHANGELOG.md in Keep a Changelog format.
- CLAUDE.md template drift check in CI.
- GitHub release creation in publish workflow.
- Tone and ordering items in pre-edit checklist.
- Tone, ordering, and changelog rules in CLAUDE.md.

### Changed

- Sort workflow template permissions alphabetically.

### Fixed

- Resolve pre-commit, commitizen, and dryclean binaries by full venv path.
- Skip GitHub setup gracefully in non-interactive shells.

## [1.0.3] - 2026-04-21

### Changed

- Sort workflow permissions alphabetically for consistency.

### Fixed

- Remove non-semver tags before build and update major version tag after publish.

## [1.0.2] - 2026-04-21

### Fixed

- Add `tag-pattern` so hatch-vcs ignores the floating `v1` action tag during build.

## [1.0.1] - 2026-04-21

### Fixed

- Restrict publish workflow trigger to semver tags only.

## [1.0.0] - 2026-04-21

### Added

- 25 custom quality check scripts (JavaScript 7, Python 11, Shell 7).
- Claude-powered PR review and description generation.
- CLI with `init`, `run`, `commit`, and `check` commands.
- GitHub Actions: `ci@v1`, `review@v1`, `describe@v1`.
- Pre-commit integration with local auto-fix and CI report-only modes.
