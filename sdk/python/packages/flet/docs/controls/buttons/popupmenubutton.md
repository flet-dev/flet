::: flet.PopupMenuButton
::: flet.PopupMenuItem

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/popupmenubutton)

### PopupMenuButton



```python
import flet as ft

def main(page: ft.Page):
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Item 1"),
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, text="Check power"),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                        ft.Text("Item with a custom content"),
                    ]
                ),
                on_click=lambda _: print("Button with a custom content clicked!"),
            ),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(
                text="Checked item", checked=False, on_click=check_item_clicked
            ),
        ]
    )
    page.add(pb)

ft.run(main)
```


<img src="/img/docs/controls/popup-menu-button/popup-menu-button-with-custom-content.gif" className="screenshot-30"/>
