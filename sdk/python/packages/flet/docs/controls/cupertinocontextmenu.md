::: flet.CupertinoContextMenu

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/cupertinocontextmenu)

### Basic Example



```python
import flet as ft


def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=ft.Image("https://picsum.photos/200/200"),
            actions=[
                ft.CupertinoContextMenuAction(
                    text="Action 1",
                    is_default_action=True,
                    trailing_icon=ft.Icons.CHECK,
                    on_click=lambda e: print("Action 1"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 2",
                    trailing_icon=ft.Icons.MORE,
                    on_click=lambda e: print("Action 2"),
                ),
                ft.CupertinoContextMenuAction(
                    text="Action 3",
                    is_destructive_action=True,
                    trailing_icon=ft.Icons.CANCEL,
                    on_click=lambda e: print("Action 3"),
                ),
            ],
        )
    )


ft.run(main)
```



<img src="/img/docs/controls/cupertino-context-menu/basic-cupertino-context-menu.gif" className="screenshot-40"/>
