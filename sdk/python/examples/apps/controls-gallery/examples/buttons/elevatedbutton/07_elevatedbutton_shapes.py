import flet as ft

name = "Buttons of different shapes"


def example():
    return ft.Column(
        controls=[
            ft.Button(
                "Stadium",
                style=ft.ButtonStyle(
                    shape=ft.StadiumBorder(),
                ),
            ),
            ft.Button(
                "Rounded rectangle",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.Button(
                "Continuous rectangle",
                style=ft.ButtonStyle(
                    shape=ft.ContinuousRectangleBorder(radius=30),
                ),
            ),
            ft.Button(
                "Beveled rectangle",
                style=ft.ButtonStyle(
                    shape=ft.BeveledRectangleBorder(radius=10),
                ),
            ),
            ft.Button(
                "Circle",
                style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=30),
            ),
        ]
    )
