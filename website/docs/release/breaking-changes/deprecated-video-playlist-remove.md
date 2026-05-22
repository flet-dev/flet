---
title: "Video.playlist_remove() deprecated"
---

# `Video.playlist_remove()` deprecated

Flet 0.85.0 deprecated
[`Video.playlist_remove()`][flet_video.Video.playlist_remove]. Mutate
[`Video.playlist`][flet_video.Video.playlist] directly instead.

The information in this guide is accurate as of Flet 0.85.0.

## Summary

Remove media items directly from `video.playlist`:

| Deprecated API | Replacement |
| --- | --- |
| `video.playlist_remove(media_index)` | `video.playlist.pop(media_index)` |

## Context

The playlist is now the source of truth for video items. Mutating the list
directly keeps the API aligned with other list-backed Flet controls.

## Migration guide

Code before migration:

```python
video.playlist_remove(media_index)
```

Code after migration:

```python
video.playlist.pop(media_index)
video.update()
```

Call `video.update()` when the mutation happens after the control has already
been added to the page.

## Timeline

- Deprecated in: `0.85.0`
- Scheduled removal: `0.88.0`

## References

- [Flet 0.85.0 announcement](/blog/flet-v-0-85-release-announcement)
- [Full changelog](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0850)
