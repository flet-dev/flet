import asyncio

import flet as ft


def main(page: ft.Page):
    page.overlay.append(hf := ft.HapticFeedback())

    page.add(
        ft.ElevatedButton(
            "Heavy impact",
            on_click=lambda: asyncio.create_task(hf.heavy_impact_async()),
        ),
        ft.ElevatedButton(
            "Medium impact",
            on_click=lambda: asyncio.create_task(hf.medium_impact_async()),
        ),
        ft.ElevatedButton(
            "Light impact",
            on_click=lambda: asyncio.create_task(hf.light_impact_async()),
        ),
        ft.ElevatedButton(
            "Vibrate", on_click=lambda: asyncio.create_task(hf.vibrate_async())
        ),
    )


ft.run(main)
