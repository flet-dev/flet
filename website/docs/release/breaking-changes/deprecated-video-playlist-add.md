---
title: "Video.playlist_add() deprecated"
---

# `Video.playlist_add()` deprecated

Flet 0.85.0 deprecated
[`Video.playlist_add()`][flet_video.Video.playlist_add]. Mutate
[`Video.playlist`][flet_video.Video.playlist] directly instead.

The information in this guide is accurate as of Flet 0.85.0.

## Summary

Append media items directly to `video.playlist`:

| Deprecated API | Replacement |
| --- | --- |
| `video.playlist_add(media)` | `video.playlist.append(media)` |

## Context

The playlist is now the source of truth for video items. Mutating the list
directly keeps the API aligned with other list-backed Flet controls.

## Migration guide

Code before migration:

```python
video.playlist_add(media)
```

Code after migration:

```python
video.playlist.append(media)
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
