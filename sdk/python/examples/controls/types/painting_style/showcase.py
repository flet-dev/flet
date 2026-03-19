import flet as ft
import flet.canvas as cv


def showcase_card(style: ft.PaintingStyle) -> ft.Container:
    return ft.Container(
        width=250,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(style.name, weight=ft.FontWeight.BOLD),
                cv.Canvas(
                    width=240,
                    height=110,
                    shapes=[
                        cv.Circle(
                            x=120,
                            y=55,
                            radius=34,
                            paint=ft.Paint(
                                style=style,
                                stroke_width=10,
                                color=ft.Colors.PRIMARY,
                            ),
                        )
                    ],
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="PaintingStyle Showcase")
    page.add(
        ft.Text("Compare filled vs outlined rendering for the same shape."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(style) for style in ft.PaintingStyle],
        ),
    )


ft.run(main)
