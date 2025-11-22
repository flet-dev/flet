import flet as ft

name = "Bezier curve"


def example():
    import flet.canvas as cv

    return cv.Canvas(
        [
            cv.Path(
                [
                    cv.Path.MoveTo(75, 25),
                    cv.Path.QuadraticTo(25, 25, 25, 62.5),
                    cv.Path.QuadraticTo(25, 100, 50, 100),
                    cv.Path.QuadraticTo(50, 120, 30, 125),
                    cv.Path.QuadraticTo(60, 120, 65, 100),
                    cv.Path.QuadraticTo(125, 100, 125, 62.5),
                    cv.Path.QuadraticTo(125, 25, 75, 25),
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
            cv.Path(
                [
                    cv.Path.SubPath(
                        [
                            cv.Path.MoveTo(75, 40),
                            cv.Path.CubicTo(75, 37, 70, 25, 50, 25),
                            cv.Path.CubicTo(20, 25, 20, 62.5, 20, 62.5),
                            cv.Path.CubicTo(20, 80, 40, 102, 75, 120),
                            cv.Path.CubicTo(110, 102, 130, 80, 130, 62.5),
                            cv.Path.CubicTo(130, 62.5, 130, 25, 100, 25),
                            cv.Path.CubicTo(85, 25, 75, 37, 75, 40),
                        ],
                        100,
                        100,
                    )
                ],
                paint=ft.Paint(
                    gradient=ft.PaintRadialGradient(
                        ft.Offset(150, 150), 50, [ft.Colors.PINK_100, ft.Colors.PINK]
                    ),
                    style=ft.PaintingStyle.FILL,
                ),
            ),
        ],
        width=300,
        height=300,
    )
