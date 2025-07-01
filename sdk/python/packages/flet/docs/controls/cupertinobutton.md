::: flet.CupertinoButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/cupertinobutton)

### Basic Example



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.CupertinoButton(
            content=ft.Text("Normal CupertinoButton", color=ft.CupertinoColors.DESTRUCTIVE_RED),
            opacity_on_click=0.3,
            on_click=lambda e: print("Normal CupertinoButton clicked!"),
        ),
        ft.CupertinoButton(
            content=ft.Text("Filled CupertinoButton", color=ft.Colors.YELLOW),
            bgcolor=ft.Colors.PRIMARY,
            alignment=ft.alignment.top_left,
            border_radius=ft.border_radius.all(15),
            opacity_on_click=0.5,
            on_click=lambda e: print("Filled CupertinoButton clicked!"),
        ),
        ft.ElevatedButton(
            adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
            bgcolor=ft.CupertinoColors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.Icons.FAVORITE, color="pink"),
                    ft.Text("ElevatedButton+adaptive"),
                ],
                tight=True,
            ),
        ),
    )


ft.run(main)
```


<img src="/img/docs/controls/cupertino-button/basic-cupertino-buttons.png" className="screenshot-20" />


