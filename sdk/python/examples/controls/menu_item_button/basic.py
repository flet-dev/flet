import flet as ft


def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_color_click(e: ft.Event[ft.MenuItemButton]):
        color = e.control.content.value
        background_container.content.value = f"{color} background color"
        background_container.bgcolor = color.lower()
        page.update()

    def handle_on_hover(e: ft.Event[ft.MenuItemButton]):
        print(e)

    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("BgColors"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Blue"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Green"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Red"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.RED}
                        ),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                ],
            ),
        ],
    )

    page.add(
        ft.Row(controls=[menubar]),
        background_container := ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                value="Choose a bgcolor from the menu",
                style=ft.TextStyle(weight=ft.FontWeight.W_500),
            ),
        ),
    )


ft.run(main)
