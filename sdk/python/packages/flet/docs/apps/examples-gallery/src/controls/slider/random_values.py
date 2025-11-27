import asyncio
import random

import flet as ft


async def main(page: ft.Page):
    def handle_slider_change(e: ft.Event[ft.Slider]):
        message.value = f"Slider.value changed to {e.control.value}"
        message.update()

    page.add(
        ft.Text("Slider with 'on_change' event:"),
        slider := ft.Slider(label="{value}", on_change=handle_slider_change),
        message := ft.Text(),
    )

    while True:
        await asyncio.sleep(1)
        slider.value = random.random()
        event = ft.Event("_", slider, data=slider.value)
        handle_slider_change(event)
        slider.update()


if __name__ == "__main__":
    ft.run(main)
