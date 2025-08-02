import flet as ft


def main(page: ft.Page):
    page.title = "OutlinedButton Example"

    page.add(
        ft.OutlinedButton(content="Button with icon", icon="chair_outlined"),
        ft.OutlinedButton(
            content="Button with colorful icon",
            icon="park_rounded",
            icon_color="green400",
        ),
    )


ft.run(main)
