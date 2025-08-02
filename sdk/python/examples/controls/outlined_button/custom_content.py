import flet as ft


def main(page: ft.Page):
    page.title = "OutlinedButton Example"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.OutlinedButton(
            width=150,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Icon(name=ft.Icons.FAVORITE, color=ft.Colors.PINK),
                    ft.Icon(name=ft.Icons.AUDIOTRACK, color=ft.Colors.GREEN),
                    ft.Icon(name=ft.Icons.BEACH_ACCESS, color=ft.Colors.BLUE),
                ],
            ),
        ),
        ft.OutlinedButton(
            content=ft.Container(
                padding=ft.Padding.all(10),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                    controls=[
                        ft.Text(value="Compound button", size=20),
                        ft.Text(value="This is secondary text"),
                    ],
                ),
            ),
        ),
    )


ft.run(main)
