import flet as ft


def showcase_card(size: ft.CupertinoButtonSize) -> ft.Container:
    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(size.name, weight=ft.FontWeight.BOLD),
                ft.CupertinoButton(
                    content="Continue",
                    icon=ft.CupertinoIcons.RIGHT_CHEVRON,
                    size=size,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="CupertinoButtonSize Showcase")
    page.add(
        ft.Text("Compare iOS button size presets."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(size) for size in ft.CupertinoButtonSize],
        ),
    )


ft.run(main)
