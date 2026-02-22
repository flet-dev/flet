from math import pi

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.Container(
            width=220,
            height=120,
            bgcolor=ft.Colors.BLUE_300,
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Rotate", size=28, weight=ft.FontWeight.BOLD),
            rotate=ft.Rotate(
                angle=pi / 10,
                alignment=ft.Alignment.CENTER,
                filter_quality=ft.FilterQuality.MEDIUM,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
