---
title: "InputBorder is now a class hierarchy; loose border props removed"
---

# `InputBorder` is now a class hierarchy; loose border props removed

:::note
This guide is accurate as of Flet 1.0.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 1.0.0 replaced the `InputBorder` **enum** with a hierarchy of classes that
mirrors Flutter's
[`InputBorder`](https://api.flutter.dev/flutter/material/InputBorder-class.html):

- [`OutlineInputBorder`][flet.OutlineInputBorder] — a rounded rectangle
  around all sides (`side`, `border_radius`, `gap_padding`)
- [`UnderlineInputBorder`][flet.UnderlineInputBorder] — a line along the
  bottom edge (`side`, `border_radius`)
- [`ft.InputBorder.none()`][flet.InputBorder.none] — draws nothing

At the same time, the loose border properties on `TextField`, `Dropdown`,
`DropdownM2`, and `CupertinoTextField` were **removed**: `border_radius`,
`border_width`, `border_color`, `focused_border_width`, and
`focused_border_color`. Everything they expressed (and more) now lives on the
`border` property, which accepts a single `InputBorder` or a dictionary mapping
[`ControlState`][flet.ControlState]s to `InputBorder`s.

## Background

The enum plus five loose properties could not represent Flutter's actual API:
`gap_padding` wasn't exposed, `UnderlineInputBorder`'s corner radius was
ignored, and error/disabled borders couldn't be styled at all. Each new
Flutter border property would have required another top-level control property.
The class hierarchy scales with Flutter instead: new border types, such as the
`ShapedInputBorder` added in Flutter 3.44, become new classes rather than more
properties on every form field.

## Migration guide

### Border style

Code before migration:

```python
ft.TextField(border=ft.InputBorder.OUTLINE)
ft.TextField(border=ft.InputBorder.UNDERLINE)
ft.TextField(border=ft.InputBorder.NONE)
```

Code after migration:

```python
ft.TextField(border=ft.OutlineInputBorder())  # the default; can be omitted
ft.TextField(border=ft.UnderlineInputBorder())
ft.TextField(border=ft.InputBorder.none())
```

### Corner radius, color, and width

Code before migration:

```python
ft.TextField(
    border_radius=30,
    border_color=ft.Colors.GREEN_800,
    border_width=2,
)
```

Code after migration:

```python
ft.TextField(
    border=ft.OutlineInputBorder(
        border_radius=30,
        side=ft.BorderSide(width=2, color=ft.Colors.GREEN_800),
    ),
)
```

To fully remove the border (previously `border_width=0` or
`border_color=ft.Colors.TRANSPARENT`), use `border=ft.InputBorder.none()`, or
`side=ft.BorderSide.none()` to keep the outline's shape for the fill.

Unlike the old `border_color`, an explicit `side` on a single border applies
to the **enabled** state only — the focused border stays theme-colored
(primary, 2px). To tint the focused border too, as the old code did, use the
per-state form below.

### Focused (and other per-state) borders

Code before migration:

```python
ft.TextField(
    border_radius=30,
    border_color=ft.Colors.GREEN_800,
    focused_border_color=ft.Colors.GREEN_ACCENT_400,
    focused_border_width=5,
)
```

Code after migration:

```python
ft.TextField(
    border={
        ft.ControlState.DEFAULT: ft.OutlineInputBorder(
            border_radius=30,
            side=ft.BorderSide(color=ft.Colors.GREEN_800),
        ),
        ft.ControlState.FOCUSED: ft.OutlineInputBorder(
            border_radius=30,
            side=ft.BorderSide(width=5, color=ft.Colors.GREEN_ACCENT_400),
        ),
    },
)
```

Supported state keys are `DEFAULT`, `FOCUSED`, `ERROR`, and `DISABLED` — the
error and disabled borders were not stylable before. A state entry without an
explicit `side` falls back to the `DEFAULT` entry's `side`, matching the old
`focused_border_color or border_color` **color** behavior.

The `ERROR` entry covers both error states: the field showing an error while
unfocused and while focused. When it carries no explicit `side`, the focused
variant is drawn at the thicker Material focus weight.

Note that an explicit `side` renders at exactly the width it specifies —
`ft.BorderSide` defaults to width `1`. The old implicit focused width of `2`
(applied when neither `focused_border_width` nor `border_width` was set) is
gone: pass `side=ft.BorderSide(width=2, ...)` in the `FOCUSED` entry to keep
the previous focus emphasis.

### DropdownM2 menu corners

`DropdownM2.border_radius` used to round both the input field and the open
menu. Those are now separate: `border` shapes the field, and the new
`menu_border_radius` shapes the menu. Set both to keep the old look.

Code before migration:

```python
ft.DropdownM2(border_radius=20)
```

Code after migration:

```python
ft.DropdownM2(
    border=ft.OutlineInputBorder(border_radius=20),
    menu_border_radius=20,
)
```

### Reading and comparing borders

`ft.InputBorder` is no longer an enum, so code that inspects a border rather
than setting one needs updating. There are no enum members to compare against
or iterate.

Code before migration:

```python
if field.border == ft.InputBorder.NONE:
    ...
for style in ft.InputBorder:
    ...
```

Code after migration:

```python
if field.border == ft.InputBorder.none():
    ...
for style in (
    ft.OutlineInputBorder(),
    ft.UnderlineInputBorder(),
    ft.InputBorder.none(),
):
    ...
```

Borders are compared by value, so `ft.OutlineInputBorder(border_radius=4)`
equals `ft.OutlineInputBorder()` — `4` is the default. To test only the kind of
border, use `isinstance(field.border, ft.OutlineInputBorder)`. Note that
`field.border` may also hold a `ControlState` dictionary rather than a single
border.

### Behavior changes to be aware of

- **Theme-driven border colors by default** (Material controls: `TextField`,
  `Dropdown`, `DropdownM2`). Previously the enabled border was always drawn
  black unless `border_color` was set — including in dark mode. Now a border
  without an explicit `side` lets the Material theme resolve the color and
  width per state: focused uses the primary color, error the error color, and
  the enabled color comes from the theme's outline (or, for `filled` fields,
  its active-indicator color). This is the Flutter default and works correctly
  with dark mode and custom themes.
- **An explicit `side` on a single border styles the enabled state only.**
  Previously `border_color` also tinted the focused border. Now the focused,
  error, and disabled states stay theme-resolved (focused: primary color,
  2px) unless you use the `ControlState` dictionary form — see the per-state
  example above for restoring the old focused look.
- **Underline borders now honor a corner radius.** The old `border_radius`
  prop was applied only to outlined borders and silently ignored when
  `border` was `InputBorder.UNDERLINE`. `UnderlineInputBorder.border_radius`
  is now passed through to Flutter, where it rounds the corners of the
  decoration's container — visible when the field is `filled`, because the
  fill is clipped to that radius. The border itself is still drawn as a
  single line along the bottom edge. It defaults to `4` on the top corners.
- **`CupertinoTextField`** draws a box decoration rather than a Material input
  decoration, so it translates the border differently. Leaving `border` unset
  keeps the native iOS hairline, exactly as before. Two explicit values change
  appearance: `ft.OutlineInputBorder()` without a `side` now also keeps that
  native hairline, where `InputBorder.OUTLINE` used to paint a solid black
  1px box (pass a `side` to draw your own); and `ft.InputBorder.none()` now
  actually removes the border, where `InputBorder.NONE` was silently ignored.
  An outline with an explicit `side` draws on all sides, and an underline
  draws the bottom side only, now honoring a non-default `border_radius` for
  the fill. A `border_radius` equal to the outline default (`4`) is
  indistinguishable from unset and keeps the native radius of `5`. In the
  `ControlState` dictionary form, the `DEFAULT`, `FOCUSED` and `DISABLED`
  entries apply; `ERROR` is ignored, as this control does not render an error
  state.

## Timeline

- Changed in: `1.0.0`

## References

- API documentation: [`InputBorder`][flet.InputBorder],
  [`OutlineInputBorder`][flet.OutlineInputBorder],
  [`UnderlineInputBorder`][flet.UnderlineInputBorder],
  [`ControlState`][flet.ControlState]
- [Flutter `InputBorder` API](https://api.flutter.dev/flutter/material/InputBorder-class.html)
- Release notes: [Flet 1.0.0](../../release-notes.md#10x)
