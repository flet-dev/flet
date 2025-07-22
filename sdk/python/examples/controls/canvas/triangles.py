import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.add(
        cv.Canvas(
            width=float("inf"),
            expand=True,
            shapes=[
                cv.Path(
                    paint=ft.Paint(style=ft.PaintingStyle.FILL),
                    elements=[
                        cv.Path.MoveTo(25, 25),
                        cv.Path.LineTo(105, 25),
                        cv.Path.LineTo(25, 105),
                    ],
                ),
                cv.Path(
                    paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE),
                    elements=[
                        cv.Path.MoveTo(125, 125),
                        cv.Path.LineTo(125, 45),
                        cv.Path.LineTo(45, 125),
                        cv.Path.Close(),
                    ],
                ),
            ],
        )
    )


ft.run(main)
