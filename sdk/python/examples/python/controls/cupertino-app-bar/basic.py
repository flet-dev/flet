import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = ft.CupertinoAppBar(
        leading=ft.Icon(ft.Icons.PALETTE, color=ft.Colors.ON_SECONDARY),
        title=ft.Text("CupertinoAppBar Example"),
        trailing=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, color=ft.Colors.ON_SECONDARY),
        automatic_background_visibility=False,
        bgcolor=ft.Colors.SECONDARY,
        brightness=ft.Brightness.LIGHT,
    )

    page.add(ft.Text("Body!"))


ft.run(main)
