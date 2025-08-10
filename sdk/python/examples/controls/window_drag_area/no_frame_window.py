import flet as ft


def main(page: ft.Page):
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True

    async def handle_window_close(e: ft.Event[ft.IconButton]):
        await page.window.close_async()

    page.add(
        ft.Row(
            controls=[
                ft.WindowDragArea(
                    expand=True,
                    content=ft.Container(
                        bgcolor=ft.Colors.AMBER_300,
                        padding=10,
                        content=ft.Text(
                            "Drag this area to move, maximize and "
                            "restore application window."
                        ),
                    ),
                ),
                ft.IconButton(ft.Icons.CLOSE, on_click=handle_window_close),
            ]
        )
    )


ft.run(main)
