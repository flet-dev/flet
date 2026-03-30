import flet as ft


def showcase_card(alignment: ft.CrossAxisAlignment) -> ft.Container:
    if alignment == ft.CrossAxisAlignment.STRETCH:
        preview = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=alignment,
            controls=[
                ft.Container(width=40, bgcolor=ft.Colors.PRIMARY_CONTAINER),
                ft.Container(width=40, bgcolor=ft.Colors.TERTIARY_CONTAINER),
                ft.Container(width=40, bgcolor=ft.Colors.SECONDARY_CONTAINER),
            ],
        )
    else:
        effective_alignment = (
            ft.CrossAxisAlignment.CENTER
            if alignment == ft.CrossAxisAlignment.BASELINE
            else alignment
        )
        preview = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=effective_alignment,
            controls=[
                ft.Container(
                    width=40,
                    height=24,
                    bgcolor=ft.Colors.PRIMARY_CONTAINER,
                ),
                ft.Container(
                    width=40,
                    height=46,
                    bgcolor=ft.Colors.TERTIARY_CONTAINER,
                ),
                ft.Container(
                    width=40,
                    height=34,
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                ),
            ],
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
                ft.Text(alignment.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=250,
                    height=120,
                    padding=8,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=preview,
                ),
                ft.Text(
                    "Baseline uses center fallback in this showcase.",
                    size=11,
                    visible=alignment == ft.CrossAxisAlignment.BASELINE,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="CrossAxisAlignment Showcase")
    page.add(
        ft.Text("Compare vertical alignment behavior inside the same row height."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(alignment) for alignment in ft.CrossAxisAlignment],
        ),
    )


ft.run(main)
