import flet as ft


def main(page: ft.Page):
    page.add(
        # material
        ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.FAVORITE, color=ft.Colors.PINK),
                ft.Icon(name=ft.Icons.AUDIOTRACK, color=ft.Colors.GREEN_400, size=30),
                ft.Icon(name=ft.Icons.BEACH_ACCESS, color=ft.Colors.BLUE, size=50),
                ft.Icon(name=ft.Icons.SETTINGS, color="#c1c1c1"),
            ]
        ),
        # cupertino
        ft.Row(
            controls=[
                ft.Icon(name=ft.CupertinoIcons.AIRPLANE, color=ft.Colors.PINK),
                ft.Icon(
                    name=ft.CupertinoIcons.ARROW_SWAP,
                    color=ft.Colors.GREEN_400,
                    size=30,
                ),
                ft.Icon(name=ft.CupertinoIcons.ANT, color=ft.Colors.BLUE, size=50),
                ft.Icon(name=ft.CupertinoIcons.TORTOISE, color="#c1c1c1"),
            ]
        ),
    )


ft.run(main)
