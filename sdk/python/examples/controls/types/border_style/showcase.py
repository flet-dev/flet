import flet as ft


def showcase_card(style: ft.BorderStyle) -> ft.Container:
    side = ft.BorderSide(width=4, color=ft.Colors.PRIMARY, style=style)
    border = ft.Border(left=side, top=side, right=side, bottom=side)

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
                    height=100,
                    border=border,
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Border preview"),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="BorderStyle Showcase")
    page.add(
        ft.Text("Compare rendered border sides for each BorderStyle value."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(style) for style in ft.BorderStyle],
        ),
    )


ft.run(main)
