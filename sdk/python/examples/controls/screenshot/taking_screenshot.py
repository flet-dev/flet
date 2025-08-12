from pathlib import Path

import flet as ft
from flet.utils.files import get_current_script_dir


def main(page: ft.Page):
    async def take_screenshot():
        image = await scr.capture()
        with open(Path(get_current_script_dir(), "screenshot.png"), "wb") as f:
            f.write(image)

    page.add(
        scr := ft.Screenshot(
            ft.Container(
                ft.Button("Hello, world!", bgcolor=ft.Colors.BLUE, elevation=10),
                padding=10,
            )
        ),
        ft.Button("Take screenshot", on_click=take_screenshot),
    )


ft.run(main)
