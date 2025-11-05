# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - Unreleased

### Added

- Deployed online documentation: https://docs.flet.dev/video/
- `Video` new property: `subtitle_track`
- `VideoConfiguration` new properties: `width`, `height`, `scale`

### Changed

- Refactored `Video` control to use `@flet.control` dataclass-style definition.
- Renamed `Video` event handler properties:
    - `on_loaded` → `on_load`
    - `on_completed` → `on_complete`
    - `on_track_changed` → `on_track_change`

## [0.1.0] - 2025-01-15

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-video/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-video/releases/tag/0.1.0
