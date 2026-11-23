---
title: "FluentIcons"
---

# FluentIcons

The Fluent icon set bundled with the Flutter
[`fluent_ui`](https://pub.dev/packages/fluent_ui) package, provided by the
[`flet-fluent-ui`](../index.md) package. These are the Segoe Fluent / MDL2
glyphs used across Windows.

Icons are accessed as upper snake case attributes of `FluentIcons`: the
`fluent_ui` name `chevron_down` becomes `FluentIcons.CHEVRON_DOWN`. The icons can be
browsed and searched in the [fluent_ui showcase app](https://bdlukaa.github.io/fluent_ui/).

Like [`Icons`][flet.Icons] and [`CupertinoIcons`][flet.CupertinoIcons], the
values can be used with any control that accepts an icon:

```python
import flet as ft
import flet_fluent_ui as fluent

ft.Icon(fluent.FluentIcons.HOME)
ft.IconButton(icon=fluent.FluentIcons.SETTINGS)
fluent.TextBox(placeholder="Search", suffix=fluent.FluentIcons.SEARCH)
```

`FluentIcons.random()` returns a random icon, with the same `exclude` and
`weights` arguments as `Icons.random()`.
