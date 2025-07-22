import flet as ft

name = "ResponsiveRow Example"


def example():
    return ft.Column(
        [
            ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Text("Column 1"),
                        padding=5,
                        bgcolor=ft.Colors.YELLOW,
                        col={"sm": 6, "md": 4, "xl": 2},
                    ),
                    ft.Container(
                        ft.Text("Column 2"),
                        padding=5,
                        bgcolor=ft.Colors.GREEN,
                        col={"sm": 6, "md": 4, "xl": 2},
                    ),
                    ft.Container(
                        ft.Text("Column 3"),
                        padding=5,
                        bgcolor=ft.Colors.BLUE,
                        col={"sm": 6, "md": 4, "xl": 2},
                    ),
                    ft.Container(
                        ft.Text("Column 4"),
                        padding=5,
                        bgcolor=ft.Colors.PINK_300,
                        col={"sm": 6, "md": 4, "xl": 2},
                    ),
                ],
            ),
            ft.ResponsiveRow(
                [
                    ft.TextField(label="TextField 1", col={"md": 4}),
                    ft.TextField(label="TextField 2", col={"md": 4}),
                    ft.TextField(label="TextField 3", col={"md": 4}),
                ],
                run_spacing=20,
            ),
        ]
    )
