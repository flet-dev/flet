import flet as ft


def main(page: ft.Page):
    # Yellow page theme with SYSTEM (default) mode
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.YELLOW,
    )

    page.add(
        # Page theme
        ft.Container(
            content=ft.Button("Page theme button"),
            bgcolor=ft.Colors.SURFACE_TINT,
            padding=20,
            width=300,
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
