import flet as ft


def main(page: ft.Page):
    page.title = "ElevatedButton Example"

    page.add(
        ft.ElevatedButton(
            width=150,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.PINK),
                    ft.Icon(ft.Icons.AUDIOTRACK, color=ft.Colors.GREEN),
                    ft.Icon(ft.Icons.BEACH_ACCESS, color=ft.Colors.BLUE),
                ],
            ),
        ),
        ft.ElevatedButton(
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
