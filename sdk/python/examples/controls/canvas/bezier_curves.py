import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    cp = cv.Canvas(
        width=float("inf"),
        expand=True,
        shapes=[
            cv.Path(
                paint=ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE),
                elements=[
                    cv.Path.MoveTo(x=75, y=25),
                    cv.Path.QuadraticTo(cp1x=25, cp1y=25, x=25, y=62.5),
                    cv.Path.QuadraticTo(cp1x=25, cp1y=100, x=50, y=100),
                    cv.Path.QuadraticTo(cp1x=50, cp1y=120, x=30, y=125),
                    cv.Path.QuadraticTo(cp1x=60, cp1y=120, x=65, y=100),
                    cv.Path.QuadraticTo(cp1x=125, cp1y=100, x=125, y=62.5),
                    cv.Path.QuadraticTo(cp1x=125, cp1y=25, x=75, y=25),
                ],
            ),
            cv.Path(
                elements=[
                    cv.Path.SubPath(
                        x=100,
                        y=100,
                        elements=[
                            cv.Path.MoveTo(x=75, y=40),
                            cv.Path.CubicTo(
                                cp1x=75, cp1y=37, cp2x=70, cp2y=25, x=50, y=25
                            ),
                            cv.Path.CubicTo(
                                cp1x=20, cp1y=25, cp2x=20, cp2y=62.5, x=20, y=62.5
                            ),
                            cv.Path.CubicTo(
                                cp1x=20, cp1y=80, cp2x=40, cp2y=102, x=75, y=120
                            ),
                            cv.Path.CubicTo(
                                cp1x=110, cp1y=102, cp2x=130, cp2y=80, x=130, y=62.5
                            ),
                            cv.Path.CubicTo(
                                cp1x=130, cp1y=62.5, cp2x=130, cp2y=25, x=100, y=25
                            ),
                            cv.Path.CubicTo(
                                cp1x=85, cp1y=25, cp2x=75, cp2y=37, x=75, y=40
                            ),
                        ],
                    )
                ],
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                    gradient=ft.PaintRadialGradient(
                        center=ft.Offset(150, 150),
                        radius=50,
                        colors=[ft.Colors.PINK_100, ft.Colors.PINK],
                    ),
                ),
            ),
        ],
    )

    page.add(cp)


if __name__ == "__main__":
    ft.run(main)
