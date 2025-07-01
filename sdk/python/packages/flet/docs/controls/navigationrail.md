::: flet.NavigationRail

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationrail)



```python
import flet as ft

def main(page: ft.Page):

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, label="First"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
                selected_icon=ft.Icon(ft.Icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
    )

ft.run(main)
```


<img src="/img/docs/controls/navigation-rail/custom-navrail.png" className="screenshot-50" />

## `NavigationRail` properties

### `bgcolor`

Sets the [color](/docs/reference/colors) of the Container that holds all of the NavigationRail's contents.

### `destinations`

Defines the appearance of the button items that are arrayed within the navigation rail.

The value must be a list of two or more `NavigationRailDestination` instances.

### `elevation`

Controls the size of the shadow below the NavigationRail.

Defaults to `0.0`.

### `extended`

Indicates that the NavigationRail should be in the extended state.

The extended state has a wider rail container, and the labels are positioned next to the icons. `min_extended_width` can be used to set the minimum width of the rail when it is in this state.

The rail will implicitly animate between the extended and normal state.

If the rail is going to be in the extended state, then the `label_type` must be set to `none`.

Defaults to `False`.

### `group_alignment`

The vertical alignment for the group of destinations within the rail.

The NavigationRailDestinations are grouped together with the trailing widget, between the leading widget and the bottom of the rail.

The value must be between `-1.0` and `1.0`.

If `group_alignment` is `-1.0`, then the items are aligned to the top. If `group_alignment` is `0.0`, then the items are aligned to the center. If `group_alignment` is `1.0`, then the items are aligned to the bottom.

Defaults to `-1.0`.

### `indicator_color`

The [color](/docs/reference/colors) of the navigation rail's indicator.

### `indicator_shape`

The shape of the navigation rail's indicator.

Value is of type [`OutlinedBorder`](/docs/reference/types/outlinedborder) and defaults to `StadiumBorder()`.

### `label_type`

Defines the layout and behavior of the labels for the default, unextended navigation rail.

When a navigation rail is extended, the labels are always shown.

Value is of type [`NavigationRailLabelType`](/docs/reference/types/navigationraillabeltype) and defaults to `None` - no
labels are shown.

### `leading`

An optional leading control in the rail that is placed above the destinations.

Its location is not affected by `group_alignment`.

This is commonly a [`FloatingActionButton`](/docs/controls/floatingactionbutton), but may also be a non-button, such as a logo.

### `min_extended_width`

The final width when the animation is complete for setting `extended` to `True`.

Defaults to `256`.

### `min_width`

The smallest possible width for the rail regardless of the destination's icon or label size.

Defaults to `72`.

This value also defines the min width and min height of the destinations.

To make a compact rail, set this to `56` and use `label_type='none'`.

### `selected_index`

The index into `destinations` for the current selected `NavigationRailDestination` or `None` if no destination is selected.

### `selected_label_text_style`

The [`TextStyle`](/docs/reference/types/textstyle) of a destination's label when it is selected.

When a destination is not selected, `unselected_label_text_style` will instead be used.

### `trailing`

An optional trailing control in the rail that is placed below the destinations.

Its location is affected by `group_alignment`.

This is commonly a list of additional options or destinations that is usually only rendered when `extended=True`.

### `unselected_label_text_style`

The [`TextStyle`](/docs/reference/types/textstyle) of a destination's label when it is not selected.

When a destination is selected, `selected_label_text_style` will instead be used.

## `NavigationRail` events

### `on_change`

Fires when selected destination changed.

## `NavigationRailDestination` properties

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

To make the NavigationRail more accessible, consider choosing an icon with a stroked and filled version, such as `ft.Icons.CLOUD` and `ft.Icons.CLOUD_QUEUE`. The icon should be set to the stroked version and `selected_icon` to the filled version.

### ~~`icon_content`~~

The icon `Control` of the destination. Typically the icon is an [`Icon`](/docs/controls/icon) control. Used instead of `icon` property.

**Deprecated in v0.25.0 and will be removed in v0.28.0. Use [`icon`](#icon)
instead.**

### `indicator_color`

The [color](/docs/reference/colors) of the `indicator_shape` when this destination is selected.

### `indicator_shape`

The shape of the selection indicator. The value is an instance of [`OutlinedBorder`](/docs/reference/types/outlinedborder) class.

### `label`

A string representing the destination's label. Will be displayed only if `label_content` is not provided.

### `label_content`

The label `Control` for the destination. If this is provided, then `label` will be ignored.

The label must be provided when used with the `NavigationRail`. When `NavigationRail.label_type=NavigationRailLabelType.NONE`, the label is still used for semantics, and may still be used if `NavigationRail.extended=True`.

### `padding`

The amount of space to inset the destination item.

Padding is an instance of [`Padding`](/docs/reference/types/padding) class.

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

If this icon is not provided, the NavigationRail will display `icon` in either state.

### ~~`selected_icon_content`~~

An alternative icon `Control` displayed when this destination is selected.

**Deprecated in v0.25.0 and will be removed in v0.28.0. Use [`selected_icon`](#selected_icon)
instead.**