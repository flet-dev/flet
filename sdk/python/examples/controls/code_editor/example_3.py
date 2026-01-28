import flet_code_editor as fce

import flet as ft

CODE = """# 1
# 2
# 3
import json
import textwrap

print("Folding demo")
"""


def main(page: ft.Page):
    editor = fce.CodeEditor(
        language="python",
        value=fce.TextEditingValue(
            text=CODE,
            selection=ft.TextSelection(base_offset=0, extent_offset=10),
        ),
        # read_only_section_names=["imports"],
        # visible_section_names=["main"],
        expand=True,
        on_selection_change=lambda e: print("Selection:", e.data),
    )

    async def fold_imports():
        await editor.fold_imports()

    async def fold_comment():
        await editor.fold_comment_at_line_zero()

    page.add(
        ft.Row(
            [
                ft.Button("Fold imports", on_click=fold_imports),
                ft.Button("Fold comment", on_click=fold_comment),
            ]
        ),
        editor,
    )


ft.run(main)
