import flet as ft


async def main(page: ft.Page):
    pressed_keys = set()

    def key_down(e: ft.KeyDownEvent):
        pressed_keys.add(e.key)
        keys.controls = [ft.Text(k, size=20) for k in pressed_keys]
        keys.update()

    def key_up(e: ft.KeyUpEvent):
        pressed_keys.remove(e.key)
        keys.controls = [ft.Text(k, size=20) for k in pressed_keys]
        keys.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("Press any keys..."),
                    ft.KeyboardListener(
                        autofocus=True,
                        on_key_down=key_down,
                        on_key_up=key_up,
                        content=(keys := ft.Row()),
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
