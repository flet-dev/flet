import flet as ft


def showcase_card(affinity: ft.TileAffinity) -> ft.Container:
    tile = ft.ExpansionTile(
        title="Project settings",
        subtitle="Compare where the expand arrow appears.",
        affinity=affinity,
        expanded=True,
        controls=[
            ft.ListTile(title="General"),
            ft.ListTile(title="Notifications"),
        ],
    )

    return ft.Container(
        width=360,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(affinity.name, weight=ft.FontWeight.BOLD),
                tile,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="TileAffinity Showcase")
    page.add(
        ft.Text("Compare expand-arrow placement in ExpansionTile."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(affinity) for affinity in ft.TileAffinity],
        ),
    )


ft.run(main)
