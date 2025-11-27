import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_theme_mode_toggle(e: ft.Event[ft.IconButton]):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        theme_mode_button.icon = (
            ft.Icons.WB_SUNNY_OUTLINED
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.WB_SUNNY
        )
        page.update()

    theme_mode_button = ft.IconButton(
        icon=(
            ft.Icons.WB_SUNNY_OUTLINED
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.WB_SUNNY
        ),
        icon_color=ft.Colors.ON_INVERSE_SURFACE,
        on_click=handle_theme_mode_toggle,
    )

    page.appbar = ft.CupertinoAppBar(
        automatic_background_visibility=False,
        leading=ft.Icon(ft.Icons.PALETTE, color=ft.Colors.ON_INVERSE_SURFACE),
        bgcolor=ft.Colors.INVERSE_SURFACE,
        trailing=theme_mode_button,
        title=ft.Text("CupertinoAppBar Example", color=ft.Colors.ON_INVERSE_SURFACE),
    )

    page.add(ft.Text("Body!"))


if __name__ == "__main__":
    ft.run(main)
