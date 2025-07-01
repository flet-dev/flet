::: flet.FloatingActionButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/floatingactionbutton)

### Basic FAB



```python
import flet as ft


def main(page: ft.Page):
    page.title = "Floating Action Button"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.HIDDEN
    page.appbar = ft.AppBar(
        title=ft.Text("Floating Action Button", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
        actions=[ft.IconButton(ft.Icons.MENU, tooltip="Menu", icon_color=ft.Colors.BLACK87)],
        bgcolor=ft.Colors.BLUE,
        center_title=True,
        color=ft.Colors.WHITE,
    )

    # keeps track of the number of tiles already added
    count = 0

    def fab_pressed(e):
        nonlocal count  # to modify the count variable found in the outer scope
        page.add(
            ft.ListTile(
                title=ft.Text(f"Tile {count}"),
                on_click=lambda x: print(x.control.title.value + " was clicked!"),
            )
        )
        page.open(ft.SnackBar(ft.Text("Tile was added successfully!")))
        count += 1

    page.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=fab_pressed, bgcolor=ft.Colors.LIME_300)
    page.add(ft.Text("Press the FAB to add a tile!"))


ft.run(main)
```


<img src="/img/docs/controls/floatingactionbutton/custom-fab.gif"/>
