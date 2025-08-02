import math

import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    stroke_paint = ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE)
    fill_paint = ft.Paint(style=ft.PaintingStyle.FILL)

    page.add(
        cv.Canvas(
            width=float("inf"),
            expand=True,
            shapes=[
                cv.Circle(100, 100, 50, stroke_paint),
                cv.Circle(80, 90, 10, stroke_paint),
                cv.Circle(84, 87, 5, fill_paint),
                cv.Circle(120, 90, 10, stroke_paint),
                cv.Circle(124, 87, 5, fill_paint),
                cv.Arc(70, 95, 60, 40, 0, math.pi, paint=stroke_paint),
            ],
        )
    )


ft.run(main)
