import flet as ft


def showcase_card(axis: ft.Axis) -> ft.Container:
    return ft.Container(
        width=350 if axis == ft.Axis.HORIZONTAL else 220,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(axis.name, weight=ft.FontWeight.BOLD),
                ft.SegmentedButton(
                    direction=axis,
                    selected=["medium"],
                    segments=[
                        ft.Segment(value="small", label="Small"),
                        ft.Segment(value="medium", label="Medium"),
                        ft.Segment(value="large", label="Large"),
                    ],
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="Axis Showcase")
    page.add(
        ft.Text("Compare horizontal vs vertical segment layout."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(axis) for axis in ft.Axis],
        ),
    )


ft.run(main)
