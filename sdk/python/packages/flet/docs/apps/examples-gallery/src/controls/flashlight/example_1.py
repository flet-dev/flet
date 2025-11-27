import flet as ft
import flet_flashlight as ffl


def main(page: ft.Page):
    async def toggle_flashlight():
        flashlight = ffl.Flashlight()
        await flashlight.toggle()

    page.add(ft.TextButton("toggle", on_click=toggle_flashlight))


if __name__ == "__main__":
    ft.run(main)
