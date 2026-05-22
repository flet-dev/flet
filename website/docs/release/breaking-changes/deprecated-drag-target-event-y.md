---
title: "DragTargetEvent.y deprecated"
---

# `DragTargetEvent.y` deprecated

Flet 0.85.0 deprecated [`DragTargetEvent.y`][flet.DragTargetEvent.y]. Use
[`DragTargetEvent.local_position.y`][flet.DragTargetEvent.local_position] when
you need coordinates relative to the drop target, or
[`DragTargetEvent.global_position.y`][flet.DragTargetEvent.global_position] when
you need page-level coordinates.

The information in this guide is accurate as of Flet 0.85.0.

## Summary

Replace `event.y` with the coordinate source that matches your use case:

| Deprecated API | Replacement |
| --- | --- |
| `event.y` | `event.local_position.y` or `event.global_position.y` |

## Context

`event.y` did not make the coordinate space explicit. The new position fields
separate target-relative coordinates from global coordinates, which makes drag
and drop code easier to read and less ambiguous.

## Migration guide

Code before migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_y = event.y
```

Code after migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_y = event.local_position.y
```

If your code needs page-level coordinates instead, use `event.global_position.y`.

## Timeline

- Deprecated in: `0.85.0`
- Scheduled removal: `0.88.0`

## References

- [Flet 0.85.0 announcement](/blog/flet-v-0-85-release-announcement)
- [Full changelog](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0850)
