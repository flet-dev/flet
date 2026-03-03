import flet as ft


def checkerboard() -> ft.Column:
    colors = [ft.Colors.TEAL_300, ft.Colors.AMBER_300]
    return ft.Column(
        spacing=0,
        controls=[
            ft.Row(
                spacing=0,
                controls=[
                    ft.Container(
                        width=24,
                        height=24,
                        bgcolor=colors[(row + col) % 2],
                    )
                    for col in range(9)
                ],
            )
            for row in range(6)
        ],
    )


def showcase_card(mode: ft.BlurTileMode) -> ft.Container:
    preview = ft.Container(
        width=216,
        height=144,
        border_radius=8,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Stack(
            controls=[
                checkerboard(),
                ft.Container(
                    left=8,
                    top=28,
                    width=120,
                    height=80,
                    blur=ft.Blur(8, 8, mode),
                    bgcolor="#55FFFFFF",
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.WHITE),
                ),
            ]
        ),
    )

    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(mode.name, weight=ft.FontWeight.BOLD),
                preview,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="BlurTileMode Showcase")
    page.add(
        ft.Text("Compare blur edge sampling outside source bounds."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(mode) for mode in ft.BlurTileMode],
        ),
    )


ft.run(main)
