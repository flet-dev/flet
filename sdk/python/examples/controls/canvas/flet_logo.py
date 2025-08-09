import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        cv.Canvas(
            width=float("inf"),
            expand=True,
            shapes=[
                cv.Path(
                    elements=[
                        cv.Path.MoveTo(x=25, y=125),
                        cv.Path.QuadraticTo(cp1x=50, cp1y=25, x=135, y=35, w=0.35),
                        cv.Path.QuadraticTo(cp1x=75, cp1y=115, x=135, y=215, w=0.6),
                        cv.Path.QuadraticTo(cp1x=50, cp1y=225, x=25, y=125, w=0.35),
                    ],
                    paint=ft.Paint(
                        stroke_width=2,
                        style=ft.PaintingStyle.FILL,
                        color=ft.Colors.PINK_400,
                    ),
                ),
                cv.Path(
                    elements=[
                        cv.Path.MoveTo(x=85, y=125),
                        cv.Path.QuadraticTo(cp1x=120, cp1y=85, x=165, y=75, w=0.5),
                        cv.Path.QuadraticTo(cp1x=120, cp1y=115, x=165, y=175, w=0.3),
                        cv.Path.QuadraticTo(cp1x=120, cp1y=165, x=85, y=125, w=0.5),
                    ],
                    paint=ft.Paint(
                        stroke_width=2,
                        style=ft.PaintingStyle.FILL,
                        color=ft.Colors.with_opacity(0.5, ft.Colors.BLUE_400),
                    ),
                ),
            ],
        )
    )


ft.run(main)
