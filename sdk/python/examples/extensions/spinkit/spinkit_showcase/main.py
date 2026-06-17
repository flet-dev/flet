import flet_spinkit as fsk

import flet as ft


def main(page: ft.Page):
    page.title = "SpinKit"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.SafeArea(
            content=fsk.RotatingCircle(
                color=ft.Colors.BLUE,
                size=50,
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
