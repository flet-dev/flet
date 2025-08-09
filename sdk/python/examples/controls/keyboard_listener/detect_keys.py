import flet as ft


async def main(page: ft.Page):
    pressed_keys = set()

    def key_down(e: ft.KeyDownEvent):
        pressed_keys.add(e.key)
        keys.controls = [ft.Text(k, size=20) for k in pressed_keys]

    def key_up(e: ft.KeyUpEvent):
        pressed_keys.remove(e.key)
        keys.controls = [ft.Text(k, size=20) for k in pressed_keys]

    page.add(
        ft.Text("Press any keys..."),
        ft.KeyboardListener(
            content=(keys := ft.Row()),
            autofocus=True,
            on_key_down=key_down,
            on_key_up=key_up,
        ),
    )


ft.run(main)
