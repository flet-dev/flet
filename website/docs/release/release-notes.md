---
title: "Release notes"
---

# Release notes

This page links the narrative release announcement, the product changelog, and
the migration notes for each Flet release.

## 0.85.1

- [Changelog](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0851)

### Highlights

- Fixed `TooltipTheme.decoration` for controls using `ft.Tooltip(...)`.
- Fixed `flet-geolocator` reliability on web and desktop.
- Fixed Pyodide dependency markers for `oauthlib` and `httpx`.

## 0.85.0

- [Announcement](/blog/flet-v-0-85-release-announcement)
- [Changelog](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0850)
- [Breaking changes and migration](breaking-changes/0-85.md)
- [Deprecations](deprecations.md#deprecated-in-0850)

### Highlights

- Declarative [`Router`][flet.Router] for `@ft.component` apps.
- Declarative dialog state with [`use_dialog()`][flet.use_dialog].
- Configurable [`Video.controls`][flet_video.Video.controls],
  [`Video.take_screenshot()`][flet_video.Video.take_screenshot],
  [`Video.on_position_change`][flet_video.Video.on_position_change], and
  [`Video.on_duration_change`][flet_video.Video.on_duration_change].
- PCM16 streaming and direct upload for [`AudioRecorder`][flet_audio_recorder.AudioRecorder].
- Scrollable [`NavigationRail`][flet.NavigationRail] and scroll support for
  [`ResponsiveRow`][flet.ResponsiveRow].

### Migration impact

- Deprecated `DragTargetEvent.x`, `DragTargetEvent.y`, and
  `DragTargetEvent.offset`.
- Deprecated `Video.show_controls`, `Video.playlist_add()`, and
  `Video.playlist_remove()`.
- Removed deprecated module-level helper functions from `ft.margin`,
  `ft.padding`, `ft.border`, and `ft.border_radius`.
