import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Text(
            spans=[
                ft.TextSpan(
                    text="Greetings, planet!",
                    style=ft.TextStyle(
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                begin=(0, 20),
                                end=(150, 20),
                                colors=[ft.Colors.RED, ft.Colors.YELLOW],
                            )
                        ),
                    ),
                ),
            ],
        )
    )


ft.run(main)
