::: flet.Banner

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/banner)

### Banner with leading icon and actions



```python
import flet as ft


def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def close_banner(e):
        page.close(banner)
        page.add(ft.Text("Action clicked: " + e.control.text))

    action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)
    banner = ft.Banner(
        bgcolor=ft.Colors.AMBER_100,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
        content=ft.Text(
            value="Oops, there were some errors while trying to delete the file. What would you like me to do?",
            color=ft.Colors.BLACK,
        ),
        actions=[
            ft.TextButton(text="Retry", style=action_button_style, on_click=close_banner),
            ft.TextButton(text="Ignore", style=action_button_style, on_click=close_banner),
            ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
        ],
    )

    page.add(ft.ElevatedButton("Show Banner", on_click=lambda e: page.open(banner)))


ft.run(main)
```


<img src="/img/docs/controls/banner/banner-with-custom-content.gif" className="screenshot-40"/>
