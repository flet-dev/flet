import flet as ft


def main(page: ft.Page):
    # page.theme = ft.Theme(
    #     color_scheme_seed=ft.Colors.YELLOW,
    #     color_scheme=ft.ColorScheme(
    #         primary=ft.Colors.GREEN, primary_container=ft.Colors.GREEN_200
    #     ),
    # )

    page.add(
        ft.Row(
            controls=[
                ft.Button("Page theme"),
                ft.TextButton("Page theme text button"),
                ft.Text(
                    "Text in primary container color",
                    color=ft.Colors.PRIMARY_CONTAINER,
                ),
            ]
        ),
        ft.Container(
            height=100,
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
            content=ft.Row(
                controls=[
                    ft.Button("Inherited theme with primary color overridden"),
                    ft.TextButton("Button 2"),
                ]
            ),
        ),
        ft.Container(
            padding=20,
            bgcolor=ft.Colors.SURFACE_TINT,
            theme_mode=ft.ThemeMode.DARK,
            theme=ft.Theme(
                color_scheme_seed=ft.Colors.GREEN,
                color_scheme=ft.ColorScheme(primary_container=ft.Colors.BLUE),
            ),
            content=ft.Row(
                controls=[
                    ft.Button("Always DARK theme"),
                    ft.TextButton("Text button"),
                    ft.Text(
                        "Text in primary container color",
                        color=ft.Colors.PRIMARY_CONTAINER,
                    ),
                ]
            ),
        ),
        ft.Container(
            padding=20,
            bgcolor=ft.Colors.SURFACE_TINT,
            border=ft.Border.all(3, ft.Colors.OUTLINE),
            theme_mode=ft.ThemeMode.LIGHT,
            theme=ft.Theme(),
            content=ft.Row(
                controls=[
                    ft.Button("Always LIGHT theme"),
                    ft.TextButton("Text button"),
                    ft.Text(
                        "Text in primary container color",
                        color=ft.Colors.PRIMARY_CONTAINER,
                    ),
                ]
            ),
        ),
        ft.Container(
            padding=20,
            bgcolor=ft.Colors.SURFACE_TINT,
            border=ft.Border.all(3, ft.Colors.OUTLINE),
            border_radius=10,
            theme_mode=ft.ThemeMode.SYSTEM,
            theme=ft.Theme(),
            content=ft.Row(
                controls=[
                    ft.Button("SYSTEM theme"),
                    ft.TextButton("Text button"),
                    ft.Text(
                        "Text in primary container color",
                        color=ft.Colors.PRIMARY_CONTAINER,
                    ),
                ]
            ),
        ),
    )


ft.run(main)
