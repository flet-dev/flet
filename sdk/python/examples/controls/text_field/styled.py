import flet as ft


def main(page: ft.Page):
    page.padding = 50

    page.add(
        ft.TextField(
            text_size=30,
            cursor_color=ft.Colors.RED,
            selection_color=ft.Colors.YELLOW,
            color=ft.Colors.PINK,
            bgcolor=ft.Colors.BLACK26,
            filled=True,
            focused_color=ft.Colors.GREEN,
            focused_bgcolor=ft.Colors.CYAN_200,
            border_radius=30,
            border_color=ft.Colors.GREEN_800,
            focused_border_color=ft.Colors.GREEN_ACCENT_400,
            max_length=20,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )
    )


ft.run(main)
