import flet as ft


def main(page: ft.Page):
    page.title = "Text selection"

    selection = ft.Text("Select some text from the field.")
    selection_details = ft.Text()
    caret = ft.Text("Caret position: -")

    def handle_selection_change(e: ft.TextSelectionChangeEvent[ft.CupertinoTextField]):
        selection.value = (
            f"Selection: '{e.selected_text}'" if e.selected_text else "No selection."
        )
        selection_details.value = f"start={e.selection.start}, end={e.selection.end}"
        caret.value = f"Caret position: {e.selection.end}"

    field = ft.CupertinoTextField(
        value="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        multiline=True,
        min_lines=3,
        autofocus=True,
        on_selection_change=handle_selection_change,
    )

    async def select_characters(_: ft.Event[ft.Button]):
        await field.focus()
        field.selection = ft.TextSelection(
            base_offset=0,
            extent_offset=len(field.value),
        )

    async def move_caret(_: ft.Event[ft.Button]):
        await field.focus()
        field.selection = ft.TextSelection(base_offset=0, extent_offset=0)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=10,
                controls=[
                    field,
                    selection,
                    selection_details,
                    caret,
                    ft.Button(content="Select all text", on_click=select_characters),
                    ft.Button(content="Move caret to start", on_click=move_caret),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
