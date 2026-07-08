---
title: "Deprecated spacing and border helper functions removed"
---

# Deprecated spacing and border helper functions removed

:::note
This guide is accurate as of Flet 0.85.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 0.85.0 removed deprecated module-level helper functions from `ft.margin`,
`ft.padding`, `ft.border`, and `ft.border_radius`.
Replace module-level helper calls with class methods:

| Removed helper                  | Replacement                    |
|---------------------------------|--------------------------------|
| `margin.all(...)`               | `Margin.all(...)`              |
| `margin.symmetric(...)`         | `Margin.symmetric(...)`        |
| `margin.only(...)`              | `Margin.only(...)`             |
| `padding.all(...)`              | `Padding.all(...)`             |
| `padding.symmetric(...)`        | `Padding.symmetric(...)`       |
| `padding.only(...)`             | `Padding.only(...)`            |
| `border.all(...)`               | `Border.all(...)`              |
| `border.symmetric(...)`         | `Border.symmetric(...)`        |
| `border.only(...)`              | `Border.only(...)`             |
| `border_radius.all(...)`        | `BorderRadius.all(...)`        |
| `border_radius.horizontal(...)` | `BorderRadius.horizontal(...)` |
| `border_radius.vertical(...)`   | `BorderRadius.vertical(...)`   |
| `border_radius.only(...)`       | `BorderRadius.only(...)`       |

## Background

The helper functions were replaced by class methods to keep the public API
consistent with the concrete value types they create. For example,
`Padding.all(...)` now clearly returns a [`Padding`][flet.Padding] value, and
`BorderRadius.only(...)` returns a [`BorderRadius`][flet.BorderRadius] value.

## Migration guide

Code before migration:

```python
import flet as ft

card = ft.Container(
    padding=ft.padding.all(12),
    border=ft.border.all(1, ft.Colors.OUTLINE),
    border_radius=ft.border_radius.all(8),
)
```

Code after migration:

```python
import flet as ft

card = ft.Container(
    padding=ft.Padding.all(12),
    border=ft.Border.all(1, ft.Colors.OUTLINE),
    border_radius=ft.BorderRadius.all(8),
)
```

## Timeline

- Removed in: `0.85.0`

## References

- API documentation: [`Border`][flet.Border], [`BorderRadius`][flet.BorderRadius], [`Padding`][flet.Padding]
- Issues and PRs: [#6425](https://github.com/flet-dev/flet/pull/6425)
- Release notes: [Flet 0.85.0](../../release-notes.md#085x)
