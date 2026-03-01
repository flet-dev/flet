import flet as ft


def showcase_card(position: ft.PopupMenuPosition) -> ft.Container:
    menu = ft.PopupMenuButton(
        menu_position=position,
        icon=ft.Text("Click me to open menu", color=ft.Colors.BLUE),
        items=[
            ft.PopupMenuItem(icon=ft.Icons.EDIT, content="Rename"),
            ft.PopupMenuItem(icon=ft.Icons.CONTENT_COPY, content="Duplicate"),
            ft.PopupMenuItem(icon=ft.Icons.DELETE, content="Delete"),
        ],
    )

    return ft.Container(
        width=300,
        height=220,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(position.name, weight=ft.FontWeight.BOLD),
                menu,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="PopupMenuPosition Showcase")
    page.add(
        ft.Text("Open each popup menu to compare their positioning."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(position) for position in ft.PopupMenuPosition],
        ),
    )


ft.run(main)
