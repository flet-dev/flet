import flet as ft


def cursor_card(cursor: ft.MouseCursor) -> ft.GestureDetector:
    return ft.GestureDetector(
        mouse_cursor=cursor,
        content=ft.Container(
            width=250,
            height=100,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=4,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(cursor.name, weight=ft.FontWeight.BOLD),
                ],
            ),
        ),
    )


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="MouseCursor Showcase")
    page.add(
        ft.Text(
            "Hover each card to compare cursor styles. "
            "Cursor rendering can vary by OS and browser.",
        ),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[cursor_card(cursor) for cursor in ft.MouseCursor],
        ),
    )


ft.run(main)
