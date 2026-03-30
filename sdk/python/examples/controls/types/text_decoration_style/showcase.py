import flet as ft


def showcase_card(style: ft.TextDecorationStyle) -> ft.Container:
    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(style.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=240,
                    height=80,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "Decorated text sample",
                        style=ft.TextStyle(
                            size=22,
                            decoration=ft.TextDecoration.UNDERLINE,
                            decoration_style=style,
                            decoration_thickness=2.4,
                            decoration_color=ft.Colors.PRIMARY,
                        ),
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="TextDecorationStyle Showcase")
    page.add(
        ft.Text("Compare underline rendering for each decoration style."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(style) for style in ft.TextDecorationStyle],
        ),
    )


ft.run(main)
