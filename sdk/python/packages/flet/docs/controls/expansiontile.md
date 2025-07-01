::: flet.ExpansionTile

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/expansiontile)

<img src="/img/docs/controls/expansion-tile/expansion-tile.png" className="screenshot-50"/>



```python
import flet as ft


def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0

    def handle_expansion_tile_change(e):
        page.open(
            ft.SnackBar(
                ft.Text(f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"),
                duration=1000,
            )
        )
        if e.control.trailing:
            e.control.trailing.name = (
                ft.Icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.Icons.ARROW_DROP_DOWN_CIRCLE
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    page.add(
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 1"),
            subtitle=ft.Text("Trailing expansion arrow icon"),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            collapsed_text_color=ft.Colors.RED,
            text_color=ft.Colors.RED,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 1"))],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 2"),
            subtitle=ft.Text("Custom expansion arrow icon"),
            trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
            collapsed_text_color=ft.Colors.GREEN,
            text_color=ft.Colors.GREEN,
            on_change=handle_expansion_tile_change,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 2"))],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 3"),
            subtitle=ft.Text("Leading expansion arrow icon"),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=True,
            collapsed_text_color=ft.Colors.BLUE,
            text_color=ft.Colors.BLUE,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        ),
    )


ft.run(main)
```
