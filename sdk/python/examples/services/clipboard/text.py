import flet as ft


async def main(page: ft.Page):
    async def set_to_clipboard():
        await ft.Clipboard().set(text_to_copy.value)
        text_to_copy.value = ""
        page.show_dialog(ft.SnackBar("Text copied to clipboard"))

    async def get_from_clipboard():
        contents = await ft.Clipboard().get()
        page.add(ft.Text(f"Clipboard contents: {contents}"))

    page.add(
        ft.Column(
            controls=[
                text_to_copy := ft.TextField(label="Text to copy"),
                ft.Button("Set to clipboard", on_click=set_to_clipboard),
                ft.Button("Get from clipboard", on_click=get_from_clipboard),
            ],
        )
    )


ft.run(main)
