import flet as ft


def showcase_card(align: ft.BorderSideStrokeAlign) -> ft.Container:
    preview = ft.Container(
        width=150,
        height=150,
        alignment=ft.Alignment.CENTER,
        content=ft.Stack(
            controls=[
                ft.Container(
                    width=90,
                    height=90,
                    border_radius=45,
                    bgcolor=ft.Colors.ON_SURFACE,
                ),
                ft.Container(
                    width=90,
                    height=90,
                    border_radius=45,
                    border=ft.Border.all(
                        side=ft.BorderSide(
                            width=18,
                            color=ft.Colors.RED,
                            stroke_align=align,
                        )
                    ),
                ),
            ],
        ),
    )

    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(align.name, weight=ft.FontWeight.BOLD),
                preview,
                ft.Text(f"value={align.value}", size=11),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="BorderSideStrokeAlign Showcase")
    page.add(
        ft.Text("Compare how thick borders are painted relative to the shape path."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(align) for align in ft.BorderSideStrokeAlign],
        ),
    )


ft.run(main)
