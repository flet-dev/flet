---
title: "LucideIcons"
---

# LucideIcons

The [Lucide](https://lucide.dev) icon set, provided by the
[`flet-shadcn-ui`](../index.md) package.

Icons are accessed as upper snake case attributes of `LucideIcons`. The Lucide
name `arrow-right` becomes `LucideIcons.ARROW_RIGHT`, and `clock-1` becomes
`LucideIcons.CLOCK_1`. Browse the available icons on
[lucide.dev/icons](https://lucide.dev/icons).

Like [`Icons`][flet.Icons] and [`CupertinoIcons`][flet.CupertinoIcons], the
values can be used with any control that accepts an icon:

```python
import flet as ft
import flet_shadcn_ui as shad

ft.Icon(shad.LucideIcons.HOUSE)
ft.IconButton(icon=shad.LucideIcons.SETTINGS)
shad.Button("Send", leading=shad.LucideIcons.SEND)
```

`LucideIcons.random()` returns a random icon, with the same `exclude` and
`weights` arguments as `Icons.random()`.
