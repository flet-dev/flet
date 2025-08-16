import flet as ft

name = "OutlinedButtons with custom content"


def example():
    return ft.Column(
        [
            ft.OutlinedButton(
                width=150,
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.FAVORITE, color="pink"),
                        ft.Icon(ft.Icons.AUDIOTRACK, color="green"),
                        ft.Icon(ft.Icons.BEACH_ACCESS, color="blue"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
            ),
            ft.OutlinedButton(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(value="Compound button", size=20),
                            ft.Text(value="This is secondary text"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    padding=ft.Padding.all(10),
                ),
            ),
        ]
    )
