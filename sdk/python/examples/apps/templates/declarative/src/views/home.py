import theme
from components.screen import Screen

import flet as ft


@ft.component
def HomeScreen():
    return Screen(
        "Home",
        tab="/",
        body=ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                tight=True,
                spacing=theme.Space.M,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        ft.Icons.WAVING_HAND_OUTLINED, size=56, color=ft.Colors.PRIMARY
                    ),
                    ft.Text("Hello from Flet!", theme_style=theme.Text.TITLE),
                    ft.Text(
                        "Start building in views/home.py.",
                        theme_style=theme.Text.BODY,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        ),
    )
