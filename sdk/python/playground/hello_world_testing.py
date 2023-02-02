import flet as ft
from playground.hello_world import HelloWorld


def main(page: ft.Page):

    button = ft.ElevatedButton(
        "Click",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: print("HA!"),
    )

    helloworld = HelloWorld()

    page.add(button, helloworld)


ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
