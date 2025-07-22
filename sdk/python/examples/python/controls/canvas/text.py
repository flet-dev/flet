import math

import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.add(
        cv.Canvas(
            width=float("inf"),
            expand=True,
            shapes=[
                cv.Text(x=0, y=0, value="Just a text"),
                cv.Circle(x=200, y=100, radius=2, paint=ft.Paint(color=ft.Colors.RED)),
                cv.Text(
                    x=200,
                    y=100,
                    style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=30),
                    alignment=ft.Alignment.TOP_CENTER,
                    rotate=math.pi * 0.15,
                    value="Rotated",
                    spans=[
                        ft.TextSpan(
                            text="around top_center",
                            style=ft.TextStyle(
                                italic=True, color=ft.Colors.GREEN, size=20
                            ),
                        )
                    ],
                ),
                cv.Circle(x=400, y=100, radius=2, paint=ft.Paint(color=ft.Colors.RED)),
                cv.Text(
                    x=400,
                    y=100,
                    value="Rotated around top_left",
                    style=ft.TextStyle(size=20),
                    alignment=ft.Alignment.TOP_LEFT,
                    rotate=math.pi * -0.15,
                ),
                cv.Circle(x=600, y=200, radius=2, paint=ft.Paint(color=ft.Colors.RED)),
                cv.Text(
                    x=600,
                    y=200,
                    value="Rotated around center",
                    style=ft.TextStyle(size=20),
                    alignment=ft.Alignment.CENTER,
                    rotate=math.pi / 2,
                ),
                cv.Text(
                    x=300,
                    y=400,
                    value="Limited to max_width and right-aligned.\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                    text_align=ft.TextAlign.RIGHT,
                    max_width=400,
                ),
                cv.Text(
                    x=200,
                    y=200,
                    value="WOW!",
                    style=ft.TextStyle(
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
                    x=200,
                    y=200,
                    value="WOW!",
                    style=ft.TextStyle(
                        weight=ft.FontWeight.BOLD,
                        size=100,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                begin=(200, 200),
                                end=(300, 300),
                                colors=[ft.Colors.YELLOW, ft.Colors.RED],
                            ),
                            stroke_join=ft.StrokeJoin.ROUND,
                            stroke_cap=ft.StrokeCap.ROUND,
                        ),
                    ),
                ),
            ],
        )
    )


ft.run(main)
