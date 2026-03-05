import flet as ft


def dot(label: str) -> ft.Container:
    return ft.Container(
        width=36,
        height=36,
        border_radius=18,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(label, size=12, color=ft.Colors.ON_PRIMARY_CONTAINER),
    )


def showcase_card(alignment: ft.MainAxisAlignment) -> ft.Container:
    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(alignment.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=250,
                    height=70,
                    padding=8,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Row(
                        alignment=alignment,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[dot("1"), dot("2"), dot("3")],
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="MainAxisAlignment Showcase")
    page.add(
        ft.Text("Compare horizontal distribution of children in a fixed-width row."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(alignment) for alignment in ft.MainAxisAlignment],
        ),
    )


ft.run(main)
