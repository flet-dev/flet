::: flet.NavigationBar

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationbar)

### A simple NavigationBar

<img src="/img/docs/controls/navigation-bar/navigation-bar-sample.gif" className="screenshot-40"/>

```python
import flet as ft

def main(page: ft.Page):

    page.title = "NavigationBar Example"
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Explore",
            ),
        ]
    )
    page.add(ft.Text("Body!"))

ft.run(main)
```
