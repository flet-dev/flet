import flet as ft

name = "Rich text with borders and stroke"


def example():
    return ft.Container(
        padding=5,
        content=ft.Stack(
            height=100,
            width=400,
            controls=[
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Greetings, planet!",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color=ft.Colors.BLUE_700,
                                    stroke_width=6,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Greetings, planet!",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_300,
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )
