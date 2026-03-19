import flet as ft


def showcase_card(alignment: ft.ListTileTitleAlignment) -> ft.Container:
    return ft.Container(
        width=380,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(alignment.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.ListTile(
                        title_alignment=alignment,
                        leading=ft.CircleAvatar(content=ft.Text("JD")),
                        title=ft.Text("Jane Doe"),
                        subtitle=ft.Text(
                            "This subtitle helps visualize vertical alignment."
                        ),
                        is_three_line=True,
                        trailing=ft.Icon(ft.Icons.MORE_VERT),
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="ListTileTitleAlignment Showcase")
    page.add(
        ft.Text("Compare leading/trailing alignment against title area."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(alignment) for alignment in ft.ListTileTitleAlignment
            ],
        ),
    )


ft.run(main)
