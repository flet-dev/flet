# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-26

## Added

- Deployed online documentation: https://flet-dev.github.io/flet-audio/

### Changed

- Refactored `Audio` control to use `@ft.control` dataclass-style definition and switched to `Service` control type.

### Breaking Changes

- `Audio` must now be added to `Page.services` instead of `Page.overlay`.
- The following properties were renamed:
    - `on_state_changed` → `on_state_change`
    - `on_duration_changed` → `on_duration_change`
    - `on_position_changed` → `on_position_change`
- Method `Audio.play()` now accepts an optional `position` parameter for specifying start position.
- The following sync methods were made [`async`](https://docs.python.org/3/library/asyncio.html):
    - `get_duration()`
    - `get_current_position()`

## [0.1.0] - 2025-01-15

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-audio/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-audio/releases/tag/0.1.0
