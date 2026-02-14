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
    page.add(
        fce.CodeEditor(
            language="python",
            code_theme="atom-one-light",
            # text_style=ft.TextStyle(font_family="monospace", size=14),
            value=CODE,
            expand=True,
            on_change=lambda e: print("Changed:", e.data),
        )
    )


ft.run(main)
