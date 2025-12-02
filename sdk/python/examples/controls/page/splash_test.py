import asyncio

import flet as ft


async def main(page: ft.Page):
    async def handle_button_click(e: ft.Event[ft.Button]):
        my_bar = ft.ProgressBar()

        page.overlay.append(my_bar)
        btn.disabled = True
        page.update()
        await asyncio.sleep(3)

        page.overlay.remove(my_bar)
        btn.disabled = False
        page.update()

    btn = ft.Button("Do some lengthy task!", on_click=handle_button_click)
    page.add(btn)


if __name__ == "__main__":
    ft.run(main)
