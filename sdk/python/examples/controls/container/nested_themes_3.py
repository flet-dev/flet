import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    def handle_switch_change(e: ft.Event[ft.Switch]):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch.thumb_icon = ft.Icons.LIGHT_MODE
        else:
            switch.thumb_icon = ft.Icons.DARK_MODE
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    # Yellow page theme with SYSTEM (default) mode
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.YELLOW)

    switch = ft.Switch(thumb_icon=ft.Icons.DARK_MODE, on_change=handle_switch_change)

    page.add(
        # Page theme
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.Button("Page theme button"),
                    bgcolor=ft.Colors.SURFACE_TINT,
                    padding=20,
                    width=300,
                ),
                ft.Container(
                    content=switch,
                    padding=ft.Padding.only(bottom=50),
                    alignment=ft.Alignment.TOP_RIGHT,
                ),
            ],
        ),
        # Inherited theme with primary color overridden
        ft.Container(
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
            content=ft.Button("Inherited theme button"),
            bgcolor=ft.Colors.SURFACE_TINT,
            padding=20,
            width=300,
        ),
        # Unique always DARK theme
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
            theme_mode=ft.ThemeMode.DARK,
            content=ft.Button("Unique theme button"),
            bgcolor=ft.Colors.SURFACE_TINT,
            padding=20,
            width=300,
        ),
    )


ft.run(main)
