#
# Run this example as a web app using the command:
#
#     flet run --web main.py
#


import flet as ft


async def main(page: ft.Page):
    bcm = ft.BrowserContextMenu()

    async def disable_context_menu():
        await bcm.disable()

    async def enable_context_menu():
        await bcm.enable()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Button(
                        "Disable browser context menu",
                        on_click=disable_context_menu,
                    ),
                    ft.Button(
                        "Enable browser context menu",
                        on_click=enable_context_menu,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
