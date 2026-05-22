---
title: "Video.show_controls deprecated"
---

# `Video.show_controls` deprecated

Flet 0.85.0 deprecated [`Video.show_controls`][flet_video.Video.show_controls].
Use [`Video.controls`][flet_video.Video.controls] instead.

The information in this guide is accurate as of Flet 0.85.0.

## Summary

Replace the boolean `show_controls` flag with the `controls` configuration:

| Deprecated API | Replacement |
| --- | --- |
| `Video.show_controls=False` | `Video.controls=None` |

## Context

`Video.controls` provides a single configuration point for built-in and custom
video controls. It also supports the old hide-controls behavior by setting the
value to `None`.

## Migration guide

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

## Timeline

- Deprecated in: `0.85.0`
- Scheduled removal: `0.88.0`

## References

- [Flet 0.85.0 announcement](/blog/flet-v-0-85-release-announcement)
- [Full changelog](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0850)
