import platform

import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50)
    version = ft.Text(f"Python {platform.python_version()}", key="python_version")

    def increment(e):
        counter.value = str(int(counter.value) + 1)
        counter.update()

    def decrement(e):
        counter.value = str(int(counter.value) - 1)
        counter.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    version,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                ft.Icons.REMOVE, key="decrement", on_click=decrement
                            ),
                            counter,
                            ft.IconButton(
                                ft.Icons.ADD, key="increment", on_click=increment
                            ),
                        ],
                    ),
                ],
            )
        )
    )


ft.run(main)
