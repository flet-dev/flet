import flet as ft


def main(page: ft.Page):
    page.overlay.append(hf := ft.HapticFeedback())

    page.add(
        ft.ElevatedButton("Heavy impact", on_click=lambda _: hf.heavy_impact()),
        ft.ElevatedButton("Medium impact", on_click=lambda _: hf.medium_impact()),
        ft.ElevatedButton("Light impact", on_click=lambda _: hf.light_impact()),
        ft.ElevatedButton("Vibrate", on_click=lambda _: hf.vibrate()),
    )


ft.run(main)
