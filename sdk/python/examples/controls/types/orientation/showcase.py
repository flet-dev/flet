from datetime import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def showcase_card(orientation: ft.Orientation) -> ft.Container:
        picker = ft.TimePicker(
            value=time(hour=10, minute=30),
            help_text=f"{orientation.name} time picker",
            orientation=orientation,
        )

        return ft.Container(
            width=300,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(orientation.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Open TimePicker",
                        icon=ft.Icons.ACCESS_TIME,
                        on_click=lambda _, p=picker: page.show_dialog(p),
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="Orientation Showcase")
    page.add(
        ft.Text("TimePicker supports PORTRAIT and LANDSCAPE layouts."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(orientation) for orientation in ft.Orientation],
        ),
    )


ft.run(main)
