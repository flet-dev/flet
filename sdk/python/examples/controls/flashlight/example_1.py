import flet_flashlight as ffl

import flet as ft


def main(page: ft.Page):
    async def toggle_flashlight():
        flashlight = ffl.Flashlight()
        await flashlight.toggle()

    page.add(ft.TextButton("toggle", on_click=toggle_flashlight))


ft.run(main)
