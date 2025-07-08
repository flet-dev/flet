::: flet.ExpansionPanelList
::: flet.ExpansionPanel

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

