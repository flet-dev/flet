import flet_code_editor as fce

import flet as ft

CODE = """import flet as ft

def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def btn_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=btn_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter,
                alignment=ft.Alignment.CENTER,
                expand=True,
            ),
            expand=True,
        ),
    )

ft.run(main)
"""


def main(page: ft.Page):
    async def handle_hide_keyboard_click(e: ft.Event[ft.IconButton]):
        # moving focus off the code editor dismisses the on-screen keyboard
        await hide_keyboard_button.focus()

    hide_keyboard_button = ft.IconButton(
        icon=ft.Icons.KEYBOARD_HIDE,
        tooltip="Hide keyboard",
        on_click=handle_hide_keyboard_click,
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        # the on-screen keyboard only exists on mobile; hiding the
                        # whole row keeps it from taking column spacing elsewhere
                        visible=page.platform.is_mobile(),
                        alignment=ft.MainAxisAlignment.END,
                        controls=[hide_keyboard_button],
                    ),
                    fce.CodeEditor(
                        language=fce.CodeLanguage.PYTHON,
                        code_theme=fce.CodeTheme.ATOM_ONE_LIGHT,
                        value=CODE,
                        expand=True,
                        on_change=lambda e: print("Changed:", e.data),
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
