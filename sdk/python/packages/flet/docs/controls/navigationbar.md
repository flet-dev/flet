::: flet.NavigationBar

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationbar)

### A simple NavigationBar

<img src="/img/docs/controls/navigation-bar/navigation-bar-sample.gif" className="screenshot-40"/>

```python
import flet as ft

def main(page: ft.Page):

    page.title = "NavigationBar Example"
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Explore",
            ),
        ]
    )
    page.add(ft.Text("Body!"))

ft.run(main)
```

## `NavigationBar` properties

### `adaptive`

If the value is `True`, an adaptive `NavigationBar` is created based on whether the target platform is iOS/macOS.

On iOS and macOS, a `CupertinoNavigationBar` is created, which has matching functionality and presentation as `NavigationBar`, and the graphics as expected on iOS. On other platforms, a Material `NavigationBar` is created.

Defaults to `False`.

### `animation_duration`

The transition time for each destination as it goes between selected and unselected.

### `bgcolor`

The [color](/docs/reference/colors) of the navigation bar itself.

### `destinations`

Defines the appearance of the button items that are arrayed within the navigation bar.

The value must be a list of two or more `NavigationBarDestination` instances.

### `elevation`

The elevation of the navigation bar itself.

### `indicator_color`

The [color](/docs/reference/colors) of the selected destination indicator.

### `indicator_shape`

The shape of the selected destination indicator.

Value is of type [`OutlinedBorder`](/docs/reference/types/outlinedborder).

### `label_behavior`

Defines how the destinations' labels will be laid out and when they'll be displayed.

Can be used to show all labels, show only the selected label, or hide all labels.

Value is of type [`NavigationBarLabelBehavior`](/docs/reference/types/navigationbarlabelbehavior) and defaults
to `NavigationBarLabelBehavior.ALWAYS_SHOW`.

### `overlay_color`

The highlight [color](/docs/reference/colors) of the `NavigationDestination` in various [`ControlState`](/docs/reference/types/controlstate) states.
The following [`ControlState`](/docs/reference/types/controlstate) values are supported: `PRESSED`, `HOVERED` and `FOCUSED`.

### `selected_index`

The index into `destinations` for the current selected `NavigationBarDestination` or `None` if no destination is selected.

### `shadow_color`

The [color](/docs/reference/colors) used for the drop shadow to indicate `elevation`.

### `surface_tint_color`

The surface tint of the Material that holds the NavigationDrawer's contents.

## `NavigationBar` events

### `on_change`

Fires when selected destination changed.

## `NavigationBarDestination` properties

### `bgcolor`

The [color](/docs/reference/colors) of this destination.

### `icon`

The [name of the icon](/docs/reference/icons) or `Control` of the destination. 

Example with icon name:
```
icon=ft.Icons.BOOKMARK
```
Example with Control:
```
icon=ft.Icon(ft.Icons.BOOKMARK)
```

If `selected_icon` is provided, this will only be displayed when the destination is not selected.

To make the NavigationBar more accessible, consider choosing an icon with a stroked and filled version, such as `ft.Icons.CLOUD` and `ft.Icons.CLOUD_QUEUE`. The icon should be set to the stroked version and `selected_icon` to the filled version.

### ~~`icon_content`~~

The icon `Control` of the destination. Typically the icon is an [`Icon`](/docs/controls/icon) control. Used instead of `icon` property.

**Deprecated in v0.25.0 and will be removed in v0.28.0. Use [`icon`](#icon)
instead.**

### `label`

The text label that appears below the icon of this `NavigationBarDestination`.

### `selected_icon`

The [name](/docs/reference/icons) of alternative icon or `Control` displayed when this destination is selected. 

Example with icon name:
```
selected_icon=ft.Icons.BOOKMARK
```
Example with Control:
```
selected_icon=ft.Icon(ft.Icons.BOOKMARK)
```

If this icon is not provided, the NavigationBar will display `icon` in either state.

### ~~`selected_icon_content`~~

An alternative icon `Control` displayed when this destination is selected.

**Deprecated in v0.25.0 and will be removed in v0.28.0. Use [`selected_icon`](#selected_icon)
instead.**