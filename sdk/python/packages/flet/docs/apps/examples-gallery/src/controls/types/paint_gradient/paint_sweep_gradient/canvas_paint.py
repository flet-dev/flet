import math

import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.add(
        cv.Canvas(
            width=float("inf"),
            expand=True,
            shapes=[
                cv.Path(
                    elements=[
                        cv.Path.Arc(
                            x=10,
                            y=230,
                            width=100,
                            height=100,
                            start_angle=3 * math.pi / 4,
                            sweep_angle=3 * math.pi / 2,
                        ),
                    ],
                    paint=ft.Paint(
                        stroke_width=15,
                        stroke_join=ft.StrokeJoin.ROUND,
                        style=ft.PaintingStyle.STROKE,
                        gradient=ft.PaintSweepGradient(
                            start_angle=0,
                            end_angle=math.pi * 2,
                            rotation=3 * math.pi / 4,
                            center=(60, 280),
                            colors=[ft.Colors.YELLOW, ft.Colors.PURPLE],
                            color_stops=[0.0, 1.0],
                        ),
                    ),
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
