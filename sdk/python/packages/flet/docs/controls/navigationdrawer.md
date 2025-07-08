::: flet.NavigationDrawer

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationdrawer)

### NavigationDrawer sliding from the left edge of a page

<img src="/img/docs/controls/navigationdrawer/navigation-drawer-start.gif" className="screenshot-60"/>

```python
import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_dismissal(e):
        page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.control.selected_index}"))
        # page.close(drawer)

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.Icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.Icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.Icons.PHONE,
            ),
        ],
    )

    page.add(ft.ElevatedButton("Show drawer", on_click=lambda e: page.open(drawer)))


ft.run(main)
```

### NavigationDrawer sliding from the right edge of a page

<img src="/img/docs/controls/navigationdrawer/navigation-drawer-end.gif" className="screenshot-60"/>

```python
import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_dismissal(e):
        page.add(ft.Text("End drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.control.selected_index}"))
        # page.close(end_drawer)

    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.NavigationDrawerDestination(icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"),
            ft.NavigationDrawerDestination(icon=ft.Icon(ft.Icons.ADD_COMMENT), label="Item 2"),
        ],
    )

    page.add(ft.ElevatedButton("Show end drawer", on_click=lambda e: page.open(end_drawer)))


ft.run(main)
```
