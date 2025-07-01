::: flet.Pagelet

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/pagelet)

### Pagelet example



```python
import flet as ft

def main(page: ft.Page):
    def open_pagelet_end_drawer(e):
        pagelet.end_drawer.open = True
        pagelet.end_drawer.update()

    pagelet = ft.Pagelet(
        appbar=ft.AppBar(
            title=ft.Text("Pagelet AppBar title"), bgcolor=ft.Colors.AMBER_ACCENT
        ),
        content=ft.Text("Pagelet body"),
        bgcolor=ft.Colors.AMBER_100,
        bottom_app_bar=ft.BottomAppBar(
            bgcolor=ft.Colors.BLUE,
            shape=ft.NotchShape.CIRCULAR,
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                    ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),
                ]
            ),
        ),
        end_drawer=ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.ADD_COMMENT, label="Item 2"
                ),
            ],
        ),
        floating_action_button=ft.FloatingActionButton(
            "Open", on_click=open_pagelet_end_drawer
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,
        width=400,
        height=400,
    )

    page.add(pagelet)


ft.run(main)
```


<img src="/img/docs/controls/pagelet/pagelet-example.png" className="screenshot-30"/>


