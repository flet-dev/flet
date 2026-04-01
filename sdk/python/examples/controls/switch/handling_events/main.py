import flet as ft


def main(page: ft.Page):
    def handle_switch_change(e: ft.Event[ft.Switch]):
        page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        e.control.label = (
            "Light ThemeMode"
            if page.theme_mode == ft.ThemeMode.LIGHT
            else "Dark ThemeMode"
        )

    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        ft.SafeArea(
            content=ft.Switch(label="Light ThemeMode", on_change=handle_switch_change)
        )
    )


if __name__ == "__main__":
    ft.run(main)
