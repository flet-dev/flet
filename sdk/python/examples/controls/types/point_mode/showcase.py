import flet as ft
import flet.canvas as cv

POINTS = [
    (25, 75),
    (70, 30),
    (115, 75),
    (160, 30),
    (205, 75),
]


def showcase_card(mode: cv.PointMode) -> ft.Container:
    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(mode.name, weight=ft.FontWeight.BOLD),
                cv.Canvas(
                    width=240,
                    height=110,
                    shapes=[
                        cv.Points(
                            points=POINTS,
                            point_mode=mode,
                            paint=ft.Paint(
                                color=ft.Colors.PRIMARY,
                                stroke_width=12,
                                stroke_cap=ft.StrokeCap.ROUND,
                            ),
                        )
                    ],
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="PointMode Showcase")
    page.add(
        ft.Text(
            "Compare how the same coordinate list is interpreted by each point mode."
        ),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(mode) for mode in cv.PointMode],
        ),
    )


ft.run(main)
