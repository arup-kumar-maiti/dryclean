# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-04-21

### Fixed

- Remove non-semver tags before build and update major version tag after publish.

### Changed

- Sort workflow permissions alphabetically for consistency.

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
