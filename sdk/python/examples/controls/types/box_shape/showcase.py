import flet as ft


def showcase_card(shape: ft.BoxShape) -> ft.Container:
    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(shape.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=200,
                    height=120,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.SURFACE,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    content=ft.Container(
                        width=120,
                        height=90,
                        alignment=ft.Alignment.CENTER,
                        shape=shape,
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                        border=ft.Border.all(2, ft.Colors.PRIMARY),
                        border_radius=(
                            ft.BorderRadius.all(16)
                            if shape == ft.BoxShape.RECTANGLE
                            else None
                        ),
                        content=ft.Text(
                            "Shape",
                            color=ft.Colors.ON_PRIMARY_CONTAINER,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="BoxShape Showcase")
    page.add(
        ft.Text("Compare rectangular and circular box decoration shapes."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(shape) for shape in ft.BoxShape],
        ),
    )


ft.run(main)
