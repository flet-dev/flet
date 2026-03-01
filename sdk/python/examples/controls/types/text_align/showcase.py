import flet as ft


def showcase_card(text_align: ft.TextAlign) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(text_align.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=240,
                    height=130,
                    padding=10,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Text(
                        text_align=text_align,
                        value="Flet helps you build cross-platform Python apps from one codebase.",  # noqa: E501
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="TextAlign Showcase")
    page.add(
        ft.Text("Compare horizontal text alignment modes in the same text block."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(text_align) for text_align in ft.TextAlign],
        ),
    )


ft.run(main)
