import flet as ft


def showcase_card(variant: ft.CardVariant) -> ft.Container:
    card = ft.Card(
        variant=variant,
        content=ft.Container(
            width=260,
            padding=12,
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text("Quarterly Report", weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Revenue increased by 18% compared to last quarter.",
                        size=12,
                    ),
                ],
            ),
        ),
    )

    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(variant.name, weight=ft.FontWeight.BOLD),
                card,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="CardVariant Showcase")
    page.add(
        ft.Text("Compare Material card visual variants."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(variant) for variant in ft.CardVariant],
        ),
    )


ft.run(main)
