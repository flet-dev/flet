import flet as ft

name = "ElevatedButtons of different shapes"


def example():
    return ft.Column(
        controls=[
            ft.ElevatedButton(
                "Stadium",
                style=ft.ButtonStyle(
                    shape=ft.StadiumBorder(),
                ),
            ),
            ft.ElevatedButton(
                "Rounded rectangle",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.ElevatedButton(
                "Continuous rectangle",
                style=ft.ButtonStyle(
                    shape=ft.ContinuousRectangleBorder(radius=30),
                ),
            ),
            ft.ElevatedButton(
                "Beveled rectangle",
                style=ft.ButtonStyle(
                    shape=ft.BeveledRectangleBorder(radius=10),
                ),
            ),
            ft.ElevatedButton(
                "Circle",
                style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=30),
            ),
        ]
    )
