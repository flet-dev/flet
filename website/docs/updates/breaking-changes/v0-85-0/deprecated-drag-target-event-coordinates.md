---
title: "DragTargetEvent coordinate fields deprecated"
---

# `DragTargetEvent` coordinate fields deprecated

:::note
This guide is accurate as of Flet 0.85.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.85.0 deprecated [`DragTargetEvent.x`][flet.DragTargetEvent.x],
[`DragTargetEvent.y`][flet.DragTargetEvent.y], and
[`DragTargetEvent.offset`][flet.DragTargetEvent.offset].

Use [`DragTargetEvent.local_position`][flet.DragTargetEvent.local_position] for
target-relative coordinates, or
[`DragTargetEvent.global_position`][flet.DragTargetEvent.global_position] for
page-level coordinates.

## Context

The old `x`, `y`, and `offset` fields did not make their coordinate space
explicit. The new position fields separate target-relative coordinates from
global coordinates, which makes drag and drop code easier to read and less
ambiguous.

## Migration guide

Code before migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_x = event.x
    target_y = event.y
    target_position = event.offset
```

Code after migration:

```python
def on_accept(event: ft.DragTargetEvent):
    target_x = event.local_position.x
    target_y = event.local_position.y
    target_position = event.local_position
```

If your code needs page-level coordinates instead, use
`event.global_position.x`, `event.global_position.y`, or
`event.global_position`.

## Timeline

- Deprecated in: `0.85.0`
- Removal in: `0.88.0`

## References

- API documentation: [`DragTargetEvent`][flet.DragTargetEvent]
- Issues and PRs: [#6387](https://github.com/flet-dev/flet/issues/6387), [#6401](https://github.com/flet-dev/flet/pull/6401)
- Release notes: [Flet 0.85.0](../../release-notes.md#085x)
