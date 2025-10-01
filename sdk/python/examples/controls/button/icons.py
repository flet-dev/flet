import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Button(content="Button with icon", icon=ft.Icons.WAVES_ROUNDED),
        ft.Button(
            content="Button with colorful icon",
            icon=ft.Icons.PARK_ROUNDED,
            icon_color=ft.Colors.GREEN_400,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
