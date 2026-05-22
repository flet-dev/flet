---
title: "DragTargetEvent.offset deprecated"
---

# `DragTargetEvent.offset` deprecated

:::warning[Important]
This guide is accurate as of Flet 0.85.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](.) lists the guides created for
each release.
:::

## Summary

Flet 0.85.0 deprecated [`DragTargetEvent.offset`][flet.DragTargetEvent.offset].
Replace `event.offset` with
[`event.local_position`][flet.DragTargetEvent.local_position] for
target-relative coordinates, or
[`event.global_position`][flet.DragTargetEvent.global_position] for page-level
coordinates.

## Context

`event.offset` did not make the coordinate space explicit. The new position
fields separate target-relative coordinates from global coordinates, which makes
drag and drop code easier to read and less ambiguous.

## Migration guide

Code before migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_position = event.offset
```

Code after migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_position = event.local_position
```

If your code needs page-level coordinates instead, use `event.global_position`.

## Timeline

- Deprecated in: `0.85.0`
- Scheduled removal: `0.88.0`

## References

- [Flet 0.85.0 release notes](../release-notes.md#0850)
- [Issue #6387](https://github.com/flet-dev/flet/issues/6387)
- [PR #6401](https://github.com/flet-dev/flet/pull/6401)
