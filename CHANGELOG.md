# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2026-04-21

### Added

- CHANGELOG.md following Keep a Changelog format.
- Tone, ordering, and changelog rules in CLAUDE.md.
- Tone and ordering items in pre-edit checklist.
- GitHub release creation in publish workflow.
- CLAUDE.md template drift check in CI.

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

- CLI with `init`, `run`, `commit`, and `check` commands.
- 25 custom quality check scripts (JavaScript 7, Python 11, Shell 7).
- GitHub Actions: `ci@v1`, `review@v1`, `describe@v1`.
- Pre-commit integration with local auto-fix and CI report-only modes.
- Claude-powered PR review and description generation.
