import flet as ft

name = "Basic usage"


def example():
    import math

    import flet.canvas as cv

    stroke_paint = ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE)
    fill_paint = ft.Paint(style=ft.PaintingStyle.FILL)

    return cv.Canvas(
        [
            cv.Circle(100, 100, 50, stroke_paint),
            cv.Circle(80, 90, 10, stroke_paint),
            cv.Circle(84, 87, 5, fill_paint),
            cv.Circle(120, 90, 10, stroke_paint),
            cv.Circle(124, 87, 5, fill_paint),
            cv.Arc(70, 95, 60, 40, 0, math.pi, paint=stroke_paint),
        ],
        width=200,
        height=200,
    )
