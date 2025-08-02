import asyncio

import flet as ft


async def main(page: ft.Page):
    page.add(ft.Text("Hello!"))
    await asyncio.sleep(3)
    page.window.visible = True
    page.update()


ft.run(main, view=ft.AppView.FLET_APP_HIDDEN)
