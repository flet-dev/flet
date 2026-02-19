import flet as ft
import flet_flashlight as ffl


@ft.component
def App():
    async def turn_on_flashlight(e):
        await ffl.Flashlight().on()

    async def turn_off_flashlight(e):
        await ffl.Flashlight().off()

    return ft.Row(
        controls=[
            ft.TextButton("On", on_click=turn_on_flashlight),
            ft.TextButton("Off", on_click=turn_off_flashlight),
        ]
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
