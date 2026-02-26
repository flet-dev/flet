import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def apply_theme_mode(theme_mode: ft.ThemeMode):
        page.theme_mode = theme_mode
        status.value = f"Active mode: {theme_mode.name}"
        page.update()

    def showcase_card(theme_mode: ft.ThemeMode) -> ft.Container:
        return ft.Container(
            width=250,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(theme_mode.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Apply",
                        on_click=lambda _, m=theme_mode: apply_theme_mode(m),
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="ThemeMode Showcase")
    page.add(
        ft.Text("Switch the app theme mode and inspect the preview below."),
        status := ft.Text(f"Active mode: {page.theme_mode.name}"),
        ft.Container(
            width=500,
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.OutlinedButton("Outlined"),
                    ft.FilledButton("Filled"),
                    ft.Switch(label="Switch", value=True),
                ],
            ),
        ),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(theme_mode) for theme_mode in ft.ThemeMode],
        ),
    )

    apply_theme_mode(ft.ThemeMode.SYSTEM)


ft.run(main)
