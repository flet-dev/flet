---
title: "Default theme surfaces are now neutral"
---

# Default theme surfaces are now neutral

:::note
This guide is accurate as of Flet 1.1.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 1.1.0 changes the colors of surfaces (page background, cards, dialogs,
menus, text fields, navigation bars and so on) in themes built from a seed
color, including the default theme an app gets when it sets no `page.theme`.

- **Before**: Material 3 tinted every surface with the seed hue. With the
  default blue seed, a "blank" light page was a lavender-tinted `#f9f9ff`-ish
  and a dark page a tinted `#131318`-ish.
- **Now**: surfaces use a neutral grey ramp with no hue - white (`#ffffff`) in
  light mode and near-black (`#121212`) in dark mode. Accent colors (primary,
  secondary, tertiary and their containers) still come from
  [`Theme.color_scheme_seed`](../../../types/theme/index.md#flet.Theme.color_scheme_seed).

The tinted look is still available with the new
[`Theme.surfaces`](../../../types/theme/index.md#flet.Theme.surfaces) property set to
[`ThemeSurfaces.TONAL`](../../../types/themesurfaces.md).

## Symptoms

No error is raised - the change is visual. An app that sets no theme, or sets
a `Theme` without `surfaces`, has a white or near-black background and grey
(instead of tinted) cards, containers, outlines and text fields after the
upgrade.

## Migration guide

To keep the seed-tinted Material 3 look, set `surfaces` to
`ThemeSurfaces.TONAL` in both the light and the dark theme:

```python
page.theme = ft.Theme(surfaces=ft.ThemeSurfaces.TONAL)
page.dark_theme = ft.Theme(surfaces=ft.ThemeSurfaces.TONAL)
```

If you set a seed color, keep it - `surfaces` only decides whether the seed
also tints surfaces:

```python
# Green accents on neutral surfaces (the new default)
page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)

# Green accents and green-tinted surfaces (the pre-1.1 look)
page.theme = ft.Theme(
    color_scheme_seed=ft.Colors.GREEN,
    surfaces=ft.ThemeSurfaces.TONAL,
)
```

### No action needed for

- Apps that already set surface colors explicitly in
  [`Theme.color_scheme`](../../../types/theme/index.md#flet.Theme.color_scheme) (for example
  `surface` or `surface_container`): explicit colors still win over both
  neutral and tonal defaults.
- Apps that already set a white or neutral background themselves.

## Timeline

- Changed in: `1.1.0`

## References

- Issue: [#6921](https://github.com/flet-dev/flet/issues/6921)
- Docs: [Theming](../../../cookbook/theming.md)
- Release notes: [Flet 1.1.0](../../release-notes.md)
