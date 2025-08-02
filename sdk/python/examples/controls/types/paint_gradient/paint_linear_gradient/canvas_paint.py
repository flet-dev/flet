import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.add(
        cv.Canvas(
            width=float("inf"),
            expand=True,
            shapes=[
                cv.Rect(
                    x=10,
                    y=10,
                    width=100,
                    height=100,
                    border_radius=5,
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                        gradient=ft.PaintLinearGradient(
                            begin=(0, 10),
                            end=(100, 50),
                            colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
                        ),
                    ),
                ),
            ],
        )
    )


ft.run(main)
