import flet as ft


def showcase_card(blend_mode: ft.BlendMode) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(blend_mode.name, weight=ft.FontWeight.BOLD),
                ft.Image(
                    src="https://picsum.photos/id/237/200/300",
                    width=240,
                    height=130,
                    fit=ft.BoxFit.COVER,
                    color=ft.Colors.LIGHT_GREEN_200,
                    color_blend_mode=blend_mode,
                    border_radius=8,
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="BlendMode Showcase")
    page.add(
        ft.Text("Compare color blending results for each BlendMode value."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(blend_mode) for blend_mode in ft.BlendMode],
        ),
    )


ft.run(main)
