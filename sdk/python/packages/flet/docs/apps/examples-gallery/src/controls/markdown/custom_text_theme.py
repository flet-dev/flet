import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    def change_theme_mode(e: ft.Event[ft.Switch]):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch.thumb_icon = ft.Icons.LIGHT_MODE
        else:
            switch.thumb_icon = ft.Icons.DARK_MODE
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    switch = ft.Switch(thumb_icon=ft.Icons.DARK_MODE, on_change=change_theme_mode)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.Markdown("I can read this!"),
                    bgcolor="#550000",
                    padding=20,
                    theme=ft.Theme(
                        text_theme=ft.TextTheme(
                            body_medium=ft.TextStyle(color=ft.Colors.WHITE),
                            body_large=ft.TextStyle(color=ft.Colors.WHITE),
                            body_small=ft.TextStyle(color=ft.Colors.WHITE),
                        )
                    ),
                ),
                ft.Container(
                    content=switch,
                    padding=ft.Padding.only(bottom=50),
                    alignment=ft.Alignment.TOP_RIGHT,
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
