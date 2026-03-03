import flet as ft


def showcase_card(mode: ft.CupertinoTimerPickerMode) -> ft.Container:
    return ft.Container(
        width=340,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(mode.name, weight=ft.FontWeight.BOLD),
                ft.CupertinoTimerPicker(
                    mode=mode,
                    value=ft.Duration(seconds=754),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="CupertinoTimerPickerMode Showcase")
    page.add(
        ft.Text("Compare timer picker layouts."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(mode) for mode in ft.CupertinoTimerPickerMode],
        ),
    )


ft.run(main)
