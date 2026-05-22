---
title: "Deprecations"
---

# Deprecations

Deprecated APIs still work for now, but they emit deprecation warnings and are
scheduled for removal. Flet normally removes deprecated APIs after three minor
releases unless a release notes page says otherwise.

API reference pages also show deprecation labels and `Deprecated` admonitions
next to the affected classes, methods, and properties.

## Deprecated in 0.85.0

| Deprecated API | Replacement | Removal version |
| --- | --- | --- |
| [`DragTargetEvent.x`][flet.DragTargetEvent.x] | [`DragTargetEvent.local_position.x`][flet.DragTargetEvent.local_position] for target-relative coordinates, or [`DragTargetEvent.global_position.x`][flet.DragTargetEvent.global_position] for global coordinates | `0.88.0` |
| [`DragTargetEvent.y`][flet.DragTargetEvent.y] | [`DragTargetEvent.local_position.y`][flet.DragTargetEvent.local_position] for target-relative coordinates, or [`DragTargetEvent.global_position.y`][flet.DragTargetEvent.global_position] for global coordinates | `0.88.0` |
| [`DragTargetEvent.offset`][flet.DragTargetEvent.offset] | [`DragTargetEvent.local_position`][flet.DragTargetEvent.local_position] for target-relative coordinates, or [`DragTargetEvent.global_position`][flet.DragTargetEvent.global_position] for global coordinates | `0.88.0` |
| [`Video.show_controls`][flet_video.Video.show_controls] | Set [`Video.controls`][flet_video.Video.controls] to `None` to hide controls | `0.88.0` |
| [`Video.playlist_add()`][flet_video.Video.playlist_add] | Mutate [`Video.playlist`][flet_video.Video.playlist] directly, for example `video.playlist.append(media)` | `0.88.0` |
| [`Video.playlist_remove()`][flet_video.Video.playlist_remove] | Mutate [`Video.playlist`][flet_video.Video.playlist] directly, for example `video.playlist.pop(media_index)` | `0.88.0` |

## Related migration guides

- [0.85 breaking changes and migration](breaking-changes/0-85.md)
