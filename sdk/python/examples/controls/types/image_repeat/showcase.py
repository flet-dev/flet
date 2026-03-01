import flet as ft


def showcase_card(repeat: ft.ImageRepeat) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(repeat.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=240,
                    height=130,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Image(
                        src="https://picsum.photos/id/237/200/300",
                        width=240,
                        height=130,
                        repeat=repeat,
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="ImageRepeat Showcase")
    page.add(
        ft.Text("Compare how an image fills uncovered space using repeat modes."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(repeat) for repeat in ft.ImageRepeat],
        ),
    )


ft.run(main)
