import flet as ft


def showcase_card(cap: ft.TextCapitalization) -> ft.Container:
    field = ft.TextField(
        width=260,
        label="Type here",
        capitalization=cap,
        border=ft.InputBorder.OUTLINE,
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
                ft.Text(cap.name, weight=ft.FontWeight.BOLD),
                field,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="TextCapitalization Showcase")
    page.add(
        ft.Text("Compare keyboard capitalization preferences for text fields."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(c) for c in ft.TextCapitalization],
        ),
    )


ft.run(main)
