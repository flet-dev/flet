import flet as ft

IMAGE_URL = "https://picsum.photos/id/1025/64/64"


def showcase_card(quality: ft.FilterQuality) -> ft.Container:
    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(quality.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=240,
                    height=120,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Image(
                        src=IMAGE_URL,
                        width=240,
                        height=120,
                        fit=ft.BoxFit.FILL,
                        filter_quality=quality,
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="FilterQuality Showcase")
    page.add(
        ft.Text("Compare image sampling quality while scaling the same source image."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(quality) for quality in ft.FilterQuality],
        ),
    )


ft.run(main)
