import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    smb = ft.SubmenuButton(
        content=ft.Text("Text Styles"),
        key="smbutton",
        menu_style=ft.MenuStyle(
            alignment=ft.Alignment.CENTER_RIGHT, side=ft.BorderSide(1)
        ),
        controls=[
            ft.MenuItemButton(
                content=ft.Text("Underlined"),
                on_click=lambda e: print(f"{e.control.content.value}.on_click"),
                style=ft.ButtonStyle(
                    text_style={
                        ft.ControlState.HOVERED: ft.TextStyle(
                            decoration=ft.TextDecoration.UNDERLINE
                        )
                    }
                ),
            ),
            ft.MenuItemButton(
                content=ft.Text("Bold"),
                on_click=lambda e: print(f"{e.control.content.value}.on_click"),
                style=ft.ButtonStyle(
                    text_style={
                        ft.ControlState.HOVERED: ft.TextStyle(weight=ft.FontWeight.BOLD)
                    }
                ),
            ),
            ft.MenuItemButton(
                content=ft.Text("Italic"),
                on_click=lambda e: print(f"{e.control.content.value}.on_click"),
                style=ft.ButtonStyle(
                    text_style={ft.ControlState.HOVERED: ft.TextStyle(italic=True)}
                ),
            ),
        ],
    )

    page.add(ft.Row(controls=[smb]))


if __name__ == "__main__":
    ft.run(main)
