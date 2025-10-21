import flet as ft


def main(page: ft.Page):
    page.title = "Text selection"
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    def handle_selection_change(e: ft.TextSelectionChangeEvent[ft.TextField]):
        selected = e.selected_text
        selection_text.value = (
            f"Selected text: '{selected}'" if selected else "No selection."
        )

        selection_details.value = f"start={e.selection.start}, end={e.selection.end}"
        caret.value = f"Caret position: {e.selection.end}"

    async def handle_programmatical_selection(e: ft.Event[ft.Button]):
        await field.focus()
        field.selection = ft.TextSelection(0, 5)

    page.add(
        ft.Column(
            spacing=10,
            controls=[
                field := ft.TextField(
                    value="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                    multiline=True,
                    min_lines=3,
                    on_selection_change=handle_selection_change,
                ),
                selection_text := ft.Text("Select some text from the field."),
                selection_details := ft.Text(),
                caret := ft.Text("Caret position: -"),
                ft.Button(
                    content="Highlight first 5 characters",
                    on_click=handle_programmatical_selection,
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
