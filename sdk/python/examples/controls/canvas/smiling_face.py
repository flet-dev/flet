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
                cv.Circle(x=100, y=100, radius=50, paint=stroke_paint),
                cv.Circle(x=80, y=90, radius=10, paint=stroke_paint),
                cv.Circle(x=84, y=87, radius=5, paint=fill_paint),
                cv.Circle(x=120, y=90, radius=10, paint=stroke_paint),
                cv.Circle(x=124, y=87, radius=5, paint=fill_paint),
                cv.Arc(
                    x=70,
                    y=95,
                    width=60,
                    height=40,
                    start_angle=0,
                    sweep_angle=math.pi,
                    paint=stroke_paint,
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
