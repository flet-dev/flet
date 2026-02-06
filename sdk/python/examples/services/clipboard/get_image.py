import flet as ft


async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def get_image_from_clipboard(e: ft.Event[ft.Button]):
        clipboard_image = await ft.Clipboard().get_image()
        if clipboard_image is None:
            status.value = "No image found in clipboard."
            preview.content = None
            return
        else:
            preview.content = ft.Image(src=clipboard_image)
            status.value = (
                f"Image loaded from clipboard ({len(clipboard_image)} bytes)."
            )

    page.add(
        ft.SafeArea(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Button(
                        "Get image from clipboard",
                        on_click=get_image_from_clipboard,
                    ),
                    status := ft.Text(),
                    preview := ft.Container(width=360, height=240),
                ],
            )
        )
    )


ft.run(main)
