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
    page.title = "CodeEditor selection"
    max_selection_preview = 80

    theme = fce.CodeTheme(
        styles={
            "keyword": ft.TextStyle(
                color=ft.Colors.INDIGO_600, weight=ft.FontWeight.W_600
            ),
            "string": ft.TextStyle(color=ft.Colors.RED_700),
            "comment": ft.TextStyle(color=ft.Colors.GREY_600, italic=True),
        }
    )

    text_style = ft.TextStyle(
        font_family="monospace",
        height=1.2,
    )

    gutter_style = fce.GutterStyle(
        text_style=ft.TextStyle(
            font_family="monospace",
            height=1.2,
        ),
        show_line_numbers=True,
        show_folding_handles=True,
        width=80,
    )

    def handle_selection_change(e: ft.TextSelectionChangeEvent[fce.CodeEditor]):
        if e.selected_text:
            normalized = " ".join(e.selected_text.split())
            suffix = "..." if len(normalized) > max_selection_preview else ""
            preview = normalized[:max_selection_preview]
            selection.value = (
                f"Selection ({len(e.selected_text)} chars): '{preview}{suffix}'"
            )
        else:
            selection.value = "No selection."
        selection_details.value = f"start={e.selection.start}, end={e.selection.end}"
        caret.value = f"Caret position: {e.selection.end}"

    async def select_all(e: ft.Event[ft.Button]):
        await editor.focus()
        editor.selection = ft.TextSelection(
            base_offset=0,
            extent_offset=len(editor.text or ""),
        )

    async def move_caret_to_start(e: ft.Event[ft.Button]):
        await editor.focus()
        editor.selection = ft.TextSelection(base_offset=0, extent_offset=0)

    page.add(
        ft.Column(
            expand=True,
            spacing=10,
            controls=[
                editor := fce.CodeEditor(
                    language="python",
                    code_theme=theme,
                    autocompletion_enabled=True,
                    autocompletion_words=[
                        "Container",
                        "Button",
                        "Text",
                        "Row",
                        "Column",
                    ],
                    text=CODE,
                    text_style=text_style,
                    gutter_style=gutter_style,
                    on_selection_change=handle_selection_change,
                    expand=True,
                ),
                selection := ft.Text("Select some text from the editor."),
                selection_details := ft.Text(),
                caret := ft.Text("Caret position: -"),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Button("Select all text", on_click=select_all),
                        ft.Button("Move caret to start", on_click=move_caret_to_start),
                    ],
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
