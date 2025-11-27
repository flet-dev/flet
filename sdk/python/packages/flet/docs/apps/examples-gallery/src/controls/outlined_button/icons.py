import flet as ft


def main(page: ft.Page):
    page.title = "OutlinedButton Example"

    page.add(
        ft.OutlinedButton(content="Button with icon", icon=ft.Icons.CHAIR_OUTLINED),
        ft.OutlinedButton(
            content="Button with colorful icon",
            icon=ft.Icons.PARK_ROUNDED,
            icon_color=ft.Colors.GREEN_400,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
