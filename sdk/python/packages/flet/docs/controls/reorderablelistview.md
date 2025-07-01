::: flet.ReorderableListView

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/autofillgroup)

### Basic example



```python
import flet as ft


def main(page: ft.Page):
    page.title = "ReorderableListView Demo"
    
    # the primary color is the color of the reorder handle
    page.theme = page.dark_theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.BLUE))

    def handle_reorder(e: ft.OnReorderEvent):
        print(f"Reordered from {e.old_index} to {e.new_index}")

    get_color = lambda i: ft.Colors.ERROR if i % 2 == 0 else ft.Colors.ON_ERROR_CONTAINER

    # horizontal
    h = ft.ReorderableListView(
        expand=True,
        horizontal=True,
        on_reorder=handle_reorder,
        controls=[
            ft.Container(
                content=ft.Text(f"Item {i}", color=ft.Colors.BLACK),
                bgcolor=get_color(i),
                margin=ft.margin.symmetric(horizontal=5, vertical=10),
                width=100,
                alignment=ft.alignment.center,
            )
            for i in range(10)
        ],
    )

    # vertical
    v = ft.ReorderableListView(
        expand=True,
        on_reorder=handle_reorder,
        controls=[
            ft.ListTile(
                title=ft.Text(f"Item {i}", color=ft.Colors.BLACK),
                leading=ft.Icon(ft.Icons.CHECK, color=ft.Colors.RED),
                bgcolor=get_color(i),
            )
            for i in range(10)
        ],
    )

    page.add(h, v)


ft.run(main)
```



<img src="/img/docs/controls/autofillgroup/autofillgroup-example.gif" className="screenshot-40"/>

