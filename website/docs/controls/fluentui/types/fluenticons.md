---
title: "FluentIcons"
---

# FluentIcons

Microsoft's [Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons),
provided by the [`flet-fluent-ui`](../index.md) package. They are the Fluent 2
icons used in Windows 11 and Microsoft 365 apps, and are MIT-licensed. The
Fluent controls draw their own icons, such as chevrons and checkmarks, from the
same set.

Most icons come in two styles: regular (outline), which is the default and
has no suffix, and filled, with a `_FILLED` suffix. The icon `chevron_down` is
`FluentIcons.CHEVRON_DOWN` and `FluentIcons.CHEVRON_DOWN_FILLED`. A few icons
come only filled, such as `FLAG_PRIDE_FILLED`. Microsoft lists the icons, with
previews, in
[regular](https://github.com/microsoft/fluentui-system-icons/blob/main/icons_regular.md)
and [filled](https://github.com/microsoft/fluentui-system-icons/blob/main/icons_filled.md)
styles: `ic_fluent_chevron_down_20_regular` there is `CHEVRON_DOWN` here, and
`ic_fluent_chevron_down_20_filled` is `CHEVRON_DOWN_FILLED`.

Like [`Icons`][flet.Icons] and [`CupertinoIcons`][flet.CupertinoIcons], the
values can be used with any control that accepts an icon:

```python
import flet as ft
import flet_fluent_ui as fluent

ft.Icon(fluent.FluentIcons.HOME)
ft.IconButton(icon=fluent.FluentIcons.SETTINGS_FILLED)
fluent.TextBox(placeholder="Search", suffix=fluent.FluentIcons.SEARCH)
```

`FluentIcons.random()` returns a random icon, with the same `exclude` and
`weights` arguments as `Icons.random()`.

## What's included

`FluentIcons` has the 2,889 icons that Microsoft draws in a single scalable
design, in regular and filled styles: about 5,700 members. Each icon is drawn
once and scaled to any size. It doesn't include:

- about 100 icons that Microsoft only draws at fixed sizes, such as `code_py`
  and `app_store`;
- the Light style, which covers about 200 icons;
- language-specific variants of a few text icons, such as bold and italic;
- product logos, which aren't part of Fluent UI System Icons.

In a web app the icon font, about 1.6 MB, is downloaded the first time an icon
from `FluentIcons` is drawn.
