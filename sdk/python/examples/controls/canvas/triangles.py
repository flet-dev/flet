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
                        cv.Path.MoveTo(x=25, y=25),
                        cv.Path.LineTo(x=105, y=25),
                        cv.Path.LineTo(x=25, y=105),
                    ],
                ),
                cv.Path(
                    paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE),
                    elements=[
                        cv.Path.MoveTo(x=125, y=125),
                        cv.Path.LineTo(x=125, y=45),
                        cv.Path.LineTo(x=45, y=125),
                        cv.Path.Close(),
                    ],
                ),
            ],
        )
    )


ft.run(main)
