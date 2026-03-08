import flet as ft
import flet.canvas as cv


def showcase_card(stroke_join: ft.StrokeJoin) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(stroke_join.name, weight=ft.FontWeight.BOLD),
                cv.Canvas(
                    width=240,
                    height=120,
                    shapes=[
                        cv.Path(
                            elements=[
                                cv.Path.MoveTo(40, 95),
                                cv.Path.LineTo(120, 25),
                                cv.Path.LineTo(200, 95),
                            ],
                            paint=ft.Paint(
                                style=ft.PaintingStyle.STROKE,
                                stroke_width=24,
                                color=ft.Colors.PRIMARY,
                                stroke_cap=ft.StrokeCap.BUTT,
                                stroke_join=stroke_join,
                            ),
                        )
                    ],
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="StrokeJoin Showcase")
    page.add(
        ft.Text("Compare corner rendering for each StrokeJoin value."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(stroke_join) for stroke_join in ft.StrokeJoin],
        ),
    )


ft.run(main)
