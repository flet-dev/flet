import flet_code_editor as fce

import flet as ft

CODE = """# region:imports
import json
import textwrap
# endregion

# region:main
print("Folding demo")
# endregion
"""


def main(page: ft.Page):
    editor = fce.CodeEditor(
        language="python",
        value=fce.TextEditingValue(
            text=CODE,
            selection=ft.TextSelection(base_offset=0, extent_offset=0),
        ),
        read_only_section_names=["imports"],
        visible_section_names=["main"],
        expand=True,
        on_selection_change=lambda e: print("Selection:", e.data),
    )

    async def fold_imports(_: ft.ControlEvent):
        await editor.fold_imports()

    async def fold_comment(_: ft.ControlEvent):
        await editor.fold_comment_at_line_zero()

    page.add(
        ft.Row(
            [
                ft.ElevatedButton("Fold imports", on_click=fold_imports),
                ft.ElevatedButton("Fold comment", on_click=fold_comment),
            ]
        ),
        editor,
    )


ft.run(main)
