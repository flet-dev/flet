---
title: "DragTargetEvent.offset deprecated"
---

# `DragTargetEvent.offset` deprecated

Flet 0.85.0 deprecated [`DragTargetEvent.offset`][flet.DragTargetEvent.offset].
Use [`DragTargetEvent.local_position`][flet.DragTargetEvent.local_position] for
coordinates relative to the drop target, or
[`DragTargetEvent.global_position`][flet.DragTargetEvent.global_position] for
page-level coordinates.

The information in this guide is accurate as of Flet 0.85.0.

## Summary

Replace `event.offset` with the coordinate source that matches your use case:

| Deprecated API | Replacement |
| --- | --- |
| `event.offset` | `event.local_position` or `event.global_position` |

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

- [Flet 0.85.0 announcement](/blog/flet-v-0-85-release-announcement)
- [Full changelog](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0850)
