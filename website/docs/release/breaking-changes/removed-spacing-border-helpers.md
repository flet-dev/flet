---
title: "Deprecated spacing and border helper functions removed"
---

# Deprecated spacing and border helper functions removed

:::warning[Important]
This guide is accurate as of Flet 0.85.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](.) lists the guides created for
each release.
:::

## Summary

Flet 0.85.0 removed deprecated module-level helper functions from `ft.margin`,
`ft.padding`, `ft.border`, and `ft.border_radius`.
Replace module-level helper calls with class methods:

| Removed helper | Replacement |
| --- | --- |
| `ft.margin.all(...)` | `ft.Margin.all(...)` |
| `ft.margin.symmetric(...)` | `ft.Margin.symmetric(...)` |
| `ft.margin.only(...)` | `ft.Margin.only(...)` |
| `ft.padding.all(...)` | `ft.Padding.all(...)` |
| `ft.padding.symmetric(...)` | `ft.Padding.symmetric(...)` |
| `ft.padding.only(...)` | `ft.Padding.only(...)` |
| `ft.border.all(...)` | `ft.Border.all(...)` |
| `ft.border.symmetric(...)` | `ft.Border.symmetric(...)` |
| `ft.border.only(...)` | `ft.Border.only(...)` |
| `ft.border_radius.all(...)` | `ft.BorderRadius.all(...)` |
| `ft.border_radius.horizontal(...)` | `ft.BorderRadius.horizontal(...)` |
| `ft.border_radius.vertical(...)` | `ft.BorderRadius.vertical(...)` |
| `ft.border_radius.only(...)` | `ft.BorderRadius.only(...)` |

## Background

The helper functions were replaced by class methods to keep the public API
consistent with the concrete value types they create. For example,
`ft.Padding.all(...)` now clearly returns a [`Padding`][flet.Padding] value, and
`ft.BorderRadius.only(...)` returns a [`BorderRadius`][flet.BorderRadius] value.

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
- Stable release: `0.85.0`

## References

- [Flet 0.85.0 release notes](../release-notes.md#0850)
- [PR #6425](https://github.com/flet-dev/flet/pull/6425)
