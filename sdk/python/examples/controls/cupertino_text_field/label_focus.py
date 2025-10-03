import flet as ft


async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        ctf := ft.CupertinoTextField(
            label="Textfield Label",
        )
    )
    await ctf.focus()


ft.run(main)
