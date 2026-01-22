# Changelog

## [2.1.2] - 2026-01-22

* Added: Export history to CSV

## [2.1.1] - 2026-01-22

### Added

* Selenium + pytest E2E harness (local server fixtures, page object)
* Negative-path test coverage (custom symbols empty)

### Improved

* Accessibility automation via axe (WCAG A/AA)
* Core generator logic section marked as stable (freeze markers)

### Fixed

* Ignore macOS .DS_Store and other dev artifacts

## [2.1.0] - 2026-01-21

### Added

* Site policy presets (quick configuration for picky websites)
* Batch generation (1/5/10/20)
* Session history (recent passwords with Copy/Use, Clear)
* Local settings persistence (localStorage)
* Help modal + usage info

### Improved

* Copy UX feedback
* Strength indicator (reduced screen reader noise)
* Layout at 200% zoom (scrollable, responsive card)

### Testing

* Selenium E2E harness (pytest)
* Axe accessibility checks (WCAG A/AA)
* GitHub Actions workflow (CI)

