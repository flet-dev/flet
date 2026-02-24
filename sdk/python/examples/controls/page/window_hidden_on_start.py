#
# Use -n (--hidden) option to run this example with `flet run` command:
#
#     flet run --hidden window_hidden_on_start.py
#

import asyncio

import flet as ft


async def main(page: ft.Page):
    print("Window is hidden on start. Will show after 3 seconds...")
    page.add(ft.Text("Hello!"))

    # some configuration that we want to do before showing the window
    page.window.width = 300
    page.window.height = 200
    page.update()
    await page.window.center()

    # wait for 3 seconds before showing the window
    await asyncio.sleep(3)

    # show the window
    page.window.visible = True
    page.update()


ft.run(main, view=ft.AppView.FLET_APP_HIDDEN)
