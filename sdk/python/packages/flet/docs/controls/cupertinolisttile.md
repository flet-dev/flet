::: flet.CupertinoListTile

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/cupertinolisttile)



```python
import flet as ft


def main(page: ft.Page):
    def tile_clicked(e):
        print("Tile clicked")

    page.add(
        ft.CupertinoListTile(
            additional_info=ft.Text("Wed Jan 24"),
            bgcolor_activated=ft.Colors.AMBER_ACCENT,
            leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
            title=ft.Text("CupertinoListTile not notched"),
            subtitle=ft.Text("Subtitle"),
            trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
            on_click=tile_clicked,
        ),
        ft.CupertinoListTile(
            notched=True,
            additional_info=ft.Text("Thu Jan 25"),
            leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
            title=ft.Text("CupertinoListTile notched"),
            subtitle=ft.Text("Subtitle"),
            trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
            on_click=tile_clicked,
        ),
    )


ft.run(main)
```


<img src="/img/docs/controls/cupertinolisttile/cupertinolisttile-example.png" className="screenshot-70"/>
