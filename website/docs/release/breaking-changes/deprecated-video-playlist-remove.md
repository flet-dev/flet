---
title: "Video.playlist_remove() deprecated"
---

# `Video.playlist_remove()` deprecated

:::warning[Important]
This guide is accurate as of Flet 0.85.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](.) lists the guides created for
each release.
:::

## Summary

Flet 0.85.0 deprecated
[`Video.playlist_remove()`][flet_video.Video.playlist_remove].
Remove media items directly from [`Video.playlist`][flet_video.Video.playlist]
with `video.playlist.pop(media_index)`.

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

- [Flet 0.85.0 release notes](../release-notes.md#0850)
- [PR #6463](https://github.com/flet-dev/flet/pull/6463)
