import flet as ft


def showcase_card(scroll_mode: ft.ScrollMode) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(scroll_mode.name, weight=ft.FontWeight.BOLD),
                ft.Text("Scroll inside this panel", size=12),
                ft.Container(
                    height=170,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    padding=8,
                    content=ft.Column(
                        spacing=4,
                        scroll=scroll_mode,
                        controls=[ft.Text(f"Item {i + 1}") for i in range(24)],
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="ScrollMode Showcase")
    page.add(
        ft.Text("Compare scrollbar visibility and scrolling behavior modes."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(scroll_mode) for scroll_mode in ft.ScrollMode],
        ),
    )


ft.run(main)
