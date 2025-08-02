import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Stack(
            controls=[
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            text="Greetings, planet!",
                            style=ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color=ft.Colors.BLUE_700,
                                    stroke_width=6,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            text="Greetings, planet!",
                            style=ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_300,
                            ),
                        ),
                    ],
                ),
            ]
        )
    )


ft.run(main)
