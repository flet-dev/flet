::: flet.SubmenuButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/submenubutton)

### Basic Example



```python
import flet as ft


def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0

    bg_container = ft.Ref[ft.Container]()

    def handle_color_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("BgColors"),
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("B"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Blue"),
                                style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            )
                        ]
                    ),
                    ft.SubmenuButton(
                        content=ft.Text("G"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Green"),
                                style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            )
                        ]
                    ),
                    ft.SubmenuButton(
                        content=ft.Text("R"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Red"),
                                style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.RED}),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            )
                        ]
                    )
                ]
            )
        ]
    )

    page.add(
        ft.Row([menubar]),
        ft.Container(
            ref=bg_container,
            expand=True,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Text("Choose a bgcolor from the menu", style=ft.TextThemeStyle.HEADLINE_LARGE),
            alignment=ft.alignment.center,
        )
    )


ft.run(main)
```

<img src="/img/docs/controls/submenu-button/submenu-button.gif" className="screenshot-20" />

