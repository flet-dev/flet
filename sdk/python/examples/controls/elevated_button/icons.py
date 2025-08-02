import flet as ft


def main(page: ft.Page):
    page.title = "ElevatedButton Example"

    page.add(
        ft.ElevatedButton(content="Button with icon", icon=ft.Icons.WAVES_ROUNDED),
        ft.ElevatedButton(
            content="Button with colorful icon",
            icon=ft.Icons.PARK_ROUNDED,
            icon_color=ft.Colors.GREEN_400,
        ),
    )


ft.run(main)
