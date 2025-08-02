import flet as ft


def main(page: ft.Page):
    page.padding = 30
    page.spacing = 30

    page.add(
        ft.ElevatedButton(
            content="Stadium",
            style=ft.ButtonStyle(shape=ft.StadiumBorder()),
        ),
        ft.ElevatedButton(
            content="Rounded rectangle",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        ),
        ft.ElevatedButton(
            content="Continuous rectangle",
            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)),
        ),
        ft.ElevatedButton(
            content="Beveled rectangle",
            style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=10)),
        ),
        ft.ElevatedButton(
            content="Circle",
            style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=30),
        ),
    )


ft.run(main)
