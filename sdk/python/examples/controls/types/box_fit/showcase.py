import flet as ft


def showcase_card(fit: ft.BoxFit) -> ft.Container:
    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(fit.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=240,
                    height=120,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Image(
                        src="https://picsum.photos/id/1025/420/220",
                        width=240,
                        height=120,
                        fit=fit,
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="BoxFit Showcase")
    page.add(
        ft.Text("Compare how the same image is inscribed into a fixed frame."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(fit) for fit in ft.BoxFit],
        ),
    )


ft.run(main)
