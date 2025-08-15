from typing import cast

import flet as ft


def main(page: ft.Page):
    page.add(
        # material
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.PINK),
                ft.Icon(ft.Icons.AUDIOTRACK, color=ft.Colors.GREEN_400, size=30),
                ft.Icon(ft.Icons.BEACH_ACCESS, color=ft.Colors.BLUE, size=50),
                ft.Icon(ft.Icons.SETTINGS, color="#c1c1c1"),
            ]
        ),
        # cupertino
        ft.Row(
            controls=[
                ft.Icon(ft.CupertinoIcons.PROFILE_CIRCLED, color=ft.Colors.PINK),
                ft.Icon(
                    icon=cast(ft.CupertinoIcons, ft.CupertinoIcons.random()),
                    color=ft.Colors.GREEN_400,
                    size=30,
                ),
                ft.Icon(
                    icon=cast(ft.CupertinoIcons, ft.CupertinoIcons.random()),
                    color=ft.Colors.BLUE,
                    size=50,
                ),
                ft.Icon(
                    icon=cast(ft.CupertinoIcons, ft.CupertinoIcons.random()),
                    color="#c1c1c1",
                ),
            ]
        ),
    )


if __name__ == "__main__":
    ft.run(main)
