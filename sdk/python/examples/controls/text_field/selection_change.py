import flet as ft


def main(page: ft.Page):
    page.title = "Text selection"

    def handle_selection_change(e: ft.TextSelectionChangeEvent[ft.TextField]):
        selection.value = (
            f"Selection: '{e.selected_text}'" if e.selected_text else "No selection."
        )
        selection_details.value = f"start={e.selection.start}, end={e.selection.end}"
        caret.value = f"Caret position: {e.selection.end}"

    async def select_characters(e: ft.Event[ft.Button]):
        await field.focus()
        field.selection = ft.TextSelection(
            base_offset=0, extent_offset=len(field.value)
        )

    async def move_caret(e: ft.Event[ft.Button]):
        await field.focus()
        field.selection = ft.TextSelection(base_offset=0, extent_offset=0)

    page.add(
        ft.Column(
            spacing=10,
            controls=[
                field := ft.TextField(
                    value="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                    multiline=True,
                    min_lines=3,
                    autofocus=True,
                    on_selection_change=handle_selection_change,
                ),
                selection := ft.Text("Select some text from the field."),
                selection_details := ft.Text(),
                caret := ft.Text("Caret position: -"),
                ft.Button(
                    content="Select all text",
                    on_click=select_characters,
                ),
                ft.Button(
                    content="Move caret to start",
                    on_click=move_caret,
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
