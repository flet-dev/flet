---
title: "Video.show_controls deprecated"
---

# `Video.show_controls` deprecated

:::warning[Important]
This guide is accurate as of Flet 0.85.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](.) lists the guides created for
each release.
:::

## Summary

Flet 0.85.0 deprecated [`Video.show_controls`][flet_video.Video.show_controls].
Replace the boolean `show_controls` flag with the
[`Video.controls`][flet_video.Video.controls] configuration. Set `controls` to
`None` to hide controls.

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

- [Flet 0.85.0 release notes](../release-notes.md#0850)
- [PR #6463](https://github.com/flet-dev/flet/pull/6463)
