import flet as ft

name = "Drawing text"


def example():
    import math

    import flet.canvas as cv

    return cv.Canvas(
        [
            cv.Text(0, 0, "Just a text"),
            cv.Circle(200, 100, 2, ft.Paint(color=ft.Colors.RED)),
            cv.Text(
                200,
                100,
                "Rotated",
                ft.TextStyle(weight=ft.FontWeight.BOLD, size=30),
                spans=[
                    ft.TextSpan(
                        "around top_center",
                        ft.TextStyle(italic=True, color=ft.Colors.GREEN, size=20),
                    )
                ],
                alignment=ft.Alignment.top_CENTER,
                rotate=math.pi * 0.15,
            ),
            cv.Circle(400, 100, 2, ft.Paint(color=ft.Colors.RED)),
            cv.Text(
                400,
                100,
                "Rotated around top_left",
                ft.TextStyle(size=20),
                alignment=ft.Alignment.TOP_LEFT,
                rotate=math.pi * -0.15,
            ),
            cv.Circle(600, 200, 2, ft.Paint(color=ft.Colors.RED)),
            cv.Text(
                600,
                200,
                "Rotated around center",
                ft.TextStyle(size=20),
                alignment=ft.Alignment.CENTER,
                rotate=math.pi / 2,
            ),
            cv.Text(
                300,
                400,
                "Limited to max_width and right-aligned.\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                text_align=ft.TextAlign.RIGHT,
                max_width=400,
            ),
            cv.Text(
                200,
                200,
                "WOW!",
                ft.TextStyle(
                    weight=ft.FontWeight.BOLD,
                    size=100,
                    foreground=ft.Paint(
                        color=ft.Colors.PINK,
                        stroke_width=6,
                        style=ft.PaintingStyle.STROKE,
                        stroke_join=ft.StrokeJoin.ROUND,
                        stroke_cap=ft.StrokeCap.ROUND,
                    ),
                ),
            ),
            cv.Text(
                200,
                200,
                "WOW!",
                ft.TextStyle(
                    weight=ft.FontWeight.BOLD,
                    size=100,
                    foreground=ft.Paint(
                        gradient=ft.PaintLinearGradient(
                            (200, 200),
                            (300, 300),
                            colors=[ft.Colors.YELLOW, ft.Colors.RED],
                        ),
                        stroke_join=ft.StrokeJoin.ROUND,
                        stroke_cap=ft.StrokeCap.ROUND,
                    ),
                ),
            ),
        ],
        width=700,
        height=700,
    )
