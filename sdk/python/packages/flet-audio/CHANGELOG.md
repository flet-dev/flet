# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 1.1.0

### Added

- `Audio.context` (`AudioContext`, `AudioFocus`) to configure mobile audio focus and silent mode ([#7034](https://github.com/flet-dev/flet/issues/7034), [#7041](https://github.com/flet-dev/flet/pull/7041), [#7043](https://github.com/flet-dev/flet/pull/7043)).

### Changed

- On Android, every `Audio` of an app now plays together by default, where one used to pause the others for good, and other apps' audio gets quieter instead of pausing. Set `context=AudioContext(focus=AudioFocus.GAIN)` for the previous behavior ([#7034](https://github.com/flet-dev/flet/issues/7034), [#7043](https://github.com/flet-dev/flet/pull/7043)).

### Fixed

- `Audio` failing to play when it is created without `src` and `src` is set later ([#6133](https://github.com/flet-dev/flet/issues/6133), [#6956](https://github.com/flet-dev/flet/pull/6956)).
- `Audio` ignoring `playback_rate` after `src` changes on web ([#6956](https://github.com/flet-dev/flet/pull/6956)).
- `Audio.play()`, `resume()` and `seek()` timing out on iOS when called right after creating an `Audio` with a `context`, or after `src` failed to load ([#7043](https://github.com/flet-dev/flet/pull/7043)).

## 0.85.3

### Fixed

- `Audio.play()` and `Audio.seek()` timing out when replaying after playback had completed: under the default `ReleaseMode.RELEASE`, the source is freed on completion and is now prepared again on replay ([#6536](https://github.com/flet-dev/flet/issues/6536), [#6538](https://github.com/flet-dev/flet/pull/6538)).

## 0.80.0

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

## 0.1.0

Initial release.
