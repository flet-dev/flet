---
title: "DragTargetEvent.x deprecated"
---

# `DragTargetEvent.x` deprecated

Flet 0.85.0 deprecated [`DragTargetEvent.x`][flet.DragTargetEvent.x]. Use
[`DragTargetEvent.local_position.x`][flet.DragTargetEvent.local_position] when
you need coordinates relative to the drop target, or
[`DragTargetEvent.global_position.x`][flet.DragTargetEvent.global_position] when
you need page-level coordinates.

The information in this guide is accurate as of Flet 0.85.0.

## Summary

Replace `event.x` with the coordinate source that matches your use case:

| Deprecated API | Replacement |
| --- | --- |
| `event.x` | `event.local_position.x` or `event.global_position.x` |

## Context

`event.x` did not make the coordinate space explicit. The new position fields
separate target-relative coordinates from global coordinates, which makes drag
and drop code easier to read and less ambiguous.

## Migration guide

Code before migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_x = event.x
```

Code after migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_x = event.local_position.x
```

If your code needs page-level coordinates instead, use `event.global_position.x`.

## Timeline

- Deprecated in: `0.85.0`
- Scheduled removal: `0.88.0`

## References

- [Flet 0.85.0 announcement](/blog/flet-v-0-85-release-announcement)
- [Full changelog](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0850)
