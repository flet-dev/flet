::: flet.Icon



## Examples

[Icons browser](https://gallery.flet.dev/icons-browser/)
[Live example](https://flet-controls-gallery.fly.dev/displays/icon)

### Icons of different colors and sizes



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            [
                ft.Icon(name=ft.Icons.FAVORITE, color=ft.Colors.PINK),
                ft.Icon(name=ft.Icons.AUDIOTRACK, color=ft.Colors.GREEN_400, size=30),
                ft.Icon(name=ft.Icons.BEACH_ACCESS, color=ft.Colors.BLUE, size=50),
                ft.Icon(name="settings", color="#c1c1c1"),
            ]
        )
    )

ft.run(main)
```


<img src="/img/docs/controls/icon/custom-icons.png" className="screenshot-20" />
