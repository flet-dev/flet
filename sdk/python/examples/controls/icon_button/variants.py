import flet as ft


def main(page: ft.Page):
    page.title = "IconButton variants"
    page.padding = 10
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def toggle_icon_button(e):
        e.control.selected = not e.control.selected

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50,
            controls=[
                # Normal buttons column (enabled only)
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Text(
                            "Normal",
                            theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                        ),
                        ft.FilledIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                        ),
                        ft.FilledTonalIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                        ),
                        ft.OutlinedIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                        ),
                    ],
                ),
                # Disabled buttons column
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Text(
                            "Disabled",
                            theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            disabled=True,
                        ),
                        ft.FilledIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            disabled=True,
                        ),
                        ft.FilledTonalIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            disabled=True,
                        ),
                        ft.OutlinedIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            disabled=True,
                        ),
                    ],
                ),
                # Toggle buttons column
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Text(
                            "Toggle",
                            theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            selected=False,
                            on_click=toggle_icon_button,
                        ),
                        ft.FilledIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            selected=False,
                            on_click=toggle_icon_button,
                        ),
                        ft.FilledTonalIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            selected=False,
                            on_click=toggle_icon_button,
                        ),
                        ft.OutlinedIconButton(
                            icon=ft.Icons.FILTER_DRAMA,
                            selected=False,
                            on_click=toggle_icon_button,
                        ),
                    ],
                ),
            ],
        ),
    )


ft.run(main)
