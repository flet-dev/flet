import flet as ft


def showcase_card(mode: ft.GradientTileMode) -> ft.Container:
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
                ft.Container(
                    width=240,
                    height=120,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    gradient=ft.RadialGradient(
                        radius=0.22,
                        colors=[ft.Colors.PRIMARY, ft.Colors.AMBER_400],
                        tile_mode=mode,
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="GradientTileMode Showcase")
    page.add(
        ft.Text("Compare how gradients behave outside their defined paint region."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(mode) for mode in ft.GradientTileMode],
        ),
    )


ft.run(main)
