import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.add(
        cv.Canvas(
            width=float("inf"),
            expand=True,
            shapes=[
                cv.Circle(
                    x=60,
                    y=170,
                    radius=50,
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                        gradient=ft.PaintRadialGradient(
                            radius=50,
                            center=(60, 170),
                            colors=[ft.Colors.YELLOW, ft.Colors.BLUE],
                        ),
                    ),
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
