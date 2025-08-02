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
                        cv.Path.MoveTo(25, 125),
                        cv.Path.QuadraticTo(50, 25, 135, 35, 0.35),
                        cv.Path.QuadraticTo(75, 115, 135, 215, 0.6),
                        cv.Path.QuadraticTo(50, 225, 25, 125, 0.35),
                    ],
                    paint=ft.Paint(
                        stroke_width=2,
                        style=ft.PaintingStyle.FILL,
                        color=ft.Colors.PINK_400,
                    ),
                ),
                cv.Path(
                    elements=[
                        cv.Path.MoveTo(85, 125),
                        cv.Path.QuadraticTo(120, 85, 165, 75, 0.5),
                        cv.Path.QuadraticTo(120, 115, 165, 175, 0.3),
                        cv.Path.QuadraticTo(120, 165, 85, 125, 0.5),
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
