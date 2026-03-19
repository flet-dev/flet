import flet as ft
import flet.canvas as cv


def showcase_card(stroke_cap: ft.StrokeCap) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(stroke_cap.name, weight=ft.FontWeight.BOLD),
                cv.Canvas(
                    width=240,
                    height=90,
                    shapes=[
                        cv.Line(
                            x1=40,
                            y1=45,
                            x2=200,
                            y2=45,
                            paint=ft.Paint(
                                stroke_width=24,
                                color=ft.Colors.PRIMARY,
                                stroke_cap=stroke_cap,
                            ),
                        ),
                        cv.Line(
                            x1=40,
                            y1=16,
                            x2=40,
                            y2=74,
                            paint=ft.Paint(stroke_width=2, color=ft.Colors.RED),
                        ),
                        cv.Line(
                            x1=200,
                            y1=16,
                            x2=200,
                            y2=74,
                            paint=ft.Paint(stroke_width=2, color=ft.Colors.RED),
                        ),
                    ],
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="StrokeCap Showcase")
    page.add(
        ft.Text("Compare line endings for each StrokeCap value."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(stroke_cap) for stroke_cap in ft.StrokeCap],
        ),
    )


ft.run(main)
