import flet as ft
import flet_flashlight as ffl


def main(page: ft.Page):
    async def turn_on_flashlight():
        await ffl.Flashlight().turn_on()

    async def turn_off_flashlight():
        await ffl.Flashlight().turn_off()

    page.add(
        ft.ElevatedButton("Turn On Flashlight", on_click=turn_on_flashlight),
        ft.ElevatedButton("Turn Off Flashlight", on_click=turn_off_flashlight),
    )


ft.run(main)
