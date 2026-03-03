import flet as ft


def showcase_card(overflow: ft.TextOverflow) -> ft.Container:
    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(overflow.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=250,
                    height=46,
                    padding=8,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Text(
                        "The quick brown fox jumps over the lazy dog near the Flet bridge.",  # noqa: E501
                        max_lines=1,
                        overflow=overflow,
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="TextOverflow Showcase")
    page.add(
        ft.Text("Compare how one-line text behaves when content exceeds width."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(overflow) for overflow in ft.TextOverflow],
        ),
    )


ft.run(main)
