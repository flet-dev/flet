::: flet.ExpansionPanelList

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/expansionpanellist)

### Simple Example



```python
import flet as ft


def main(page: ft.Page):
    def handle_change(e: ft.ControlEvent):
        print(f"change on panel with index {e.data}")

    def handle_delete(e: ft.ControlEvent):
        panel.controls.remove(e.control.data)
        page.update()

    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.AMBER,
        elevation=8,
        divider_color=ft.Colors.AMBER,
        on_change=handle_change,
        controls=[
            ft.ExpansionPanel(
                # has no header and content - placeholders will be used
                bgcolor=ft.Colors.BLUE_400,
                expanded=True,
            )
        ]
    )

    colors = [
        ft.Colors.GREEN_500,
        ft.Colors.BLUE_800,
        ft.Colors.RED_800,
    ]
    
    for i in range(3):
        exp = ft.ExpansionPanel(
            bgcolor=colors[i % len(colors)],
            header=ft.ListTile(title=ft.Text(f"Panel {i}")),
        )

        exp.content = ft.ListTile(
            title=ft.Text(f"This is in Panel {i}"),
            subtitle=ft.Text(f"Press the icon to delete panel {i}"),
            trailing=ft.IconButton(ft.Icons.DELETE, on_click=handle_delete, data=exp),
        )

        panel.controls.append(exp)

    page.add(panel)


ft.run(main)
```


<img src="/img/docs/controls/expansion-panel/expansion-panel.gif" className="screenshot-40"/>

## `ExpansionPanelList` Properties

### `controls`

A list of `ExpansionPanel`s to display inside `ExpansionPanelList`.

### `divider_color`

The [color](/docs/reference/colors) of the divider when `ExpansionPanel.expanded` is `False`.

### `elevation`

Defines the elevation of the children controls (`ExpansionPanel`s), while it is expanded. Default value is `2`.

### `expanded_header_padding`

Defines the padding around the header when expanded. 

Padding value is an instance of [`Padding`](/docs/reference/types/padding) class. Default value
is `padding.symmetric(vertical=16.0)`.

### `expanded_icon_color`

The [color](/docs/reference/colors) of the icon. Defaults to `colors.BLACK_54` in light theme mode and `colors.WHITE_60` in dark theme mode.

### `spacing`

The size of the gap between the `ExpansionPanel`s when expanded.

## Events

### `on_change`

Fires when an `ExpansionPanel` is expanded or collapsed. The event's data (`e.data`), contains the index of the `ExpansionPanel` which triggered this event.

## `ExpansionPanel` properties

### `bgcolor`

The background [color](/docs/reference/colors) of the panel.

### `content`

The control to be found in the body of the `ExpansionPanel`. It is displayed below the `header` when the panel is expanded.

If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as content.

### `can_tap_header`

If `True`, tapping on the panel's `header` will expand or collapse it. Defaults to `False`.

### `expanded`

Whether expanded(`True`) or collapsed(`False`). Defaults to `False`.

### `header`

The control to be found in the header of the `ExpansionPanel`. If `can_tap_header` is `True`, tapping on the header will expand or collapse the panel.

If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as header.
