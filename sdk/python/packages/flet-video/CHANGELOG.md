# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.86.2

### Fixed

- `Video.volume` (and `pitch`, `playback_rate`, `shuffle_playlist`, `playlist_mode`, `subtitle_track`) resetting to the player's defaults after toggling `visible` off then on. Showing a hidden `Video` recreates its native player at default settings; the "last-applied" tracking now lives with the player and resets on recreation, so these settings are re-applied ([#6683](https://github.com/flet-dev/flet/issues/6683), [#6694](https://github.com/flet-dev/flet/pull/6694)) by @ndonkoHenri.

## 0.85.0

### Added

- Configurable `Video.controls` with adaptive, Material, Material desktop, custom, hidden, and normal/fullscreen-specific controls ([#6463](https://github.com/flet-dev/flet/pull/6463)).
- `Video.take_screenshot()` for capturing the current video frame as PNG, JPEG, or raw BGRA bytes ([#6463](https://github.com/flet-dev/flet/pull/6463)).
- `Video.on_position_change` and `Video.on_duration_change` events emitting the current position and media duration ([#6463](https://github.com/flet-dev/flet/pull/6463)).

### Changed

- `Video.playlist` can now be mutated directly for playlist add and remove operations ([#6463](https://github.com/flet-dev/flet/pull/6463)).

### Deprecated

- `Video.playlist_add()` and `Video.playlist_remove()` are deprecated; mutate `Video.playlist` directly with list methods such as `append()` and `pop()` ([#6463](https://github.com/flet-dev/flet/pull/6463)).
- `Video.show_controls` is deprecated; set `Video.controls` to `None` to hide controls ([#6463](https://github.com/flet-dev/flet/pull/6463)).

### Fixed

- Reduce Linux memory retention when repeatedly removing `Video` controls by linking `media_kit` video apps against mimalloc in Flet run and build flows ([#6164](https://github.com/flet-dev/flet/issues/6164), [#6416](https://github.com/flet-dev/flet/pull/6416)).

## 0.80.0

### Added

- Deployed online documentation: https://flet.dev/docs/video/
- `Video` new property: `subtitle_track`
- `VideoConfiguration` new properties: `width`, `height`, `scale`

### Changed

- Refactored `Video` control to use `@flet.control` dataclass-style definition.
- Renamed `Video` event handler properties:
    - `on_loaded` → `on_load`
    - `on_completed` → `on_complete`
    - `on_track_changed` → `on_track_change`

## 0.1.0

Initial release.
