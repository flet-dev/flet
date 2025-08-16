import flet as ft


def main(page: ft.Page):
    page.overlay.append(hf := ft.HapticFeedback())

    async def heavy_impact():
        await hf.heavy_impact()

    async def medium_impact():
        await hf.medium_impact()

    async def light_impact():
        await hf.light_impact()

    async def vibrate():
        await hf.vibrate()

    page.add(
        ft.ElevatedButton("Heavy impact", on_click=heavy_impact),
        ft.ElevatedButton("Medium impact", on_click=medium_impact),
        ft.ElevatedButton("Light impact", on_click=light_impact),
        ft.ElevatedButton("Vibrate", on_click=vibrate),
    )


ft.run(main)
