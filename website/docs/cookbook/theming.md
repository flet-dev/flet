---
title: "Theming"
---

It is possible to configure your application and/or the containing controls to follow a particular themes.

### App-wide themes

The [`Page`](../controls/page.md) control (uppermost control in the tree) has two useful properties for this: [`theme`](../controls/page.md)
and [`dark_theme`](../controls/page.md) properties to configure the appearance/theme of the entire app in light and
dark theme modes respectively.

Both of type [`Theme`](../types/theme/index.md), they represent the default/fallback themes to be used app-wide,
except explicitly modified/overriden in the tree.

```python
page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
```

### Surfaces

The seed color drives accent colors (primary, secondary, tertiary and their containers).
Surfaces - page background, cards, dialogs, menus, text fields - use a neutral grey ramp:
white in light mode and near-black (`#121212`) in dark mode.

To tint surfaces with the seed hue, as in the Material 3 default color scheme, set
[`Theme.surfaces`](../types/theme/index.md#flet.Theme.surfaces) to
[`ThemeSurfaces.TONAL`](../types/themesurfaces.md):

```python
page.theme = ft.Theme(
    color_scheme_seed=ft.Colors.GREEN,
    surfaces=ft.ThemeSurfaces.TONAL,
)
```

Colors set explicitly in [`Theme.color_scheme`](../types/theme/index.md#flet.Theme.color_scheme)
always win over both neutral and tonal surfaces.

:::note
Before Flet 1.1.0, surfaces were always tinted with the seed hue. See
[Default theme surfaces are now neutral](../updates/breaking-changes/v1-1-0/neutral-default-surfaces.md).
:::

### Nested themes

You can have a part of your app to use a different theme or override some theme styles for specific controls.

Some container-like controls have `theme` and `theme_mode` properties of type
[`Theme`](../types/theme/index.md) and [`ThemeMode`](../types/thememode.md) respectively.

Specifying `theme_mode` in the `Container` means you don't want to inherit parent theme mode,
but want a completely new, unique scheme for all controls inside the container.
However, if the container does not have `theme_mode` property set then the styles from its theme property
will override the ones from the parent inherited theme:

```python
import flet as ft

def main(page: ft.Page):
    # Yellow page theme with SYSTEM (default) mode
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.YELLOW,
    )

    page.add(
        # Page theme
        ft.Container(
            content=ft.Button("Page theme button"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            width=300,
        ),

        # Inherited theme with primary color overridden
        ft.Container(
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
            content=ft.Button("Inherited theme button"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            width=300,
        ),

        # Unique always DARK theme
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
            theme_mode=ft.ThemeMode.DARK,
            content=ft.Button("Unique theme button"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            width=300,
        ),
    )

ft.run(main)
```

<figure className="doc-screenshot-figure"><img alt="Nested themes" className="doc-screenshot" src="/docs/assets/cookbook/theming/nested-themes.png" /></figure>
