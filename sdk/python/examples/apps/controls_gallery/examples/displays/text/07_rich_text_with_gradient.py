import flet as ft

name = "Rich text with gradient"


def example():
    return ft.Text(
        spans=[
            ft.TextSpan(
                "Greetings, planet!",
                ft.TextStyle(
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    foreground=ft.Paint(
                        gradient=ft.PaintLinearGradient(
                            (0, 20), (150, 20), [ft.Colors.RED, ft.Colors.YELLOW]
                        )
                    ),
                ),
            ),
        ],
    )
