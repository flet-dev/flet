import flet as ft


def showcase_card(style: ft.ListTileStyle) -> ft.Container:
    return ft.Container(
        width=360,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(style.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.ListTile(
                        style=style,
                        leading=ft.Icon(ft.Icons.PERSON),
                        title=ft.Text("Jane Doe"),
                        subtitle=ft.Text("Product Manager"),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="ListTileStyle Showcase")
    page.add(
        ft.Text("Compare list tile typography presets."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(style) for style in ft.ListTileStyle],
        ),
    )


ft.run(main)
