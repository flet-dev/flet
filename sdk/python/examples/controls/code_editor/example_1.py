import flet_code_editor as fce

import flet as ft

CODE = """def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Flet"))
"""


def main(page: ft.Page):
    page.add(
        fce.CodeEditor(
            language="python",
            theme="atom-one-light",
            text_style=ft.TextStyle(font_family="monospace", size=14),
            text=CODE,
            expand=True,
            on_change=lambda e: print("Changed:", e.data),
        )
    )


ft.run(main)
