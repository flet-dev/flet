---
title: "Video control APIs deprecated"
---

# `Video` control APIs deprecated

:::note
This guide is accurate as of Flet 0.85.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.85.0 deprecated [`Video.show_controls`][flet_video.Video.show_controls],
[`Video.playlist_add()`][flet_video.Video.playlist_add], and
[`Video.playlist_remove()`][flet_video.Video.playlist_remove].

Use [`Video.controls`][flet_video.Video.controls] to configure or hide video
controls. Mutate [`Video.playlist`][flet_video.Video.playlist] directly with
standard list methods.

## Context

`Video.controls` provides a single configuration point for built-in and custom
video controls. It also supports the old hide-controls behavior by setting the
value to `None`.

The playlist is now the source of truth for video items. Mutating the list
directly keeps the API aligned with other list-backed Flet controls.

## Migration guide

### Hiding controls

Code before migration:

```python
video = ft.Video(
    playlist=[media],
    show_controls=False,
)
```

Code after migration:

```python
video = ft.Video(
    playlist=[media],
    controls=None,
)
```

### Updating the playlist

Code before migration:

```python
video.playlist_add(media)
video.playlist_remove(media_index)
```

Code after migration:

```python
video.playlist.append(media)
video.playlist.pop(media_index)
video.update()
```

Call `video.update()` when the mutation happens after the control has already
been added to the page.

## Timeline

- Deprecated in: `0.85.0`
- Removal in: `0.88.0`

## References

- API documentation: [`Video`][flet_video.Video]
- Issues and PRs: [PR #6463](https://github.com/flet-dev/flet/pull/6463)
- Release notes: [Flet 0.85.0](../../release-notes.md#085x)
