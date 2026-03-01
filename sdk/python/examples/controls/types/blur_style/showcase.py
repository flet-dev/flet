import flet as ft


def showcase_card(style: ft.BlurStyle) -> ft.Container:
    sample = ft.Container(
        width=130,
        height=90,
        border_radius=12,
        bgcolor=ft.Colors.BLUE_400,
        shadow=ft.BoxShadow(
            blur_radius=28,
            spread_radius=3,
            color=ft.Colors.RED_400,
            offset=ft.Offset(10, 10),
            blur_style=style,
        ),
    )

    return ft.Container(
        width=300,
        height=180,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(style.name, weight=ft.FontWeight.BOLD),
                sample,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="BlurStyle Showcase")
    page.add(
        ft.Text(
            "Compare shadow blur rendering styles. "
            "The blue box uses red shadow with selected blur style."
        ),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(style) for style in ft.BlurStyle],
        ),
    )


ft.run(main)
