import flet as ft


def main(page: ft.Page):
    if page.window.width is None or page.window.height is None:
        page.add(ft.Text("Window size can be changed only in desktop apps."))
        return

    width = 400
    height = 300

    chrome_width = page.window.width - page.width
    chrome_height = page.window.height - page.height
    page.window.width = width + chrome_width
    page.window.height = height + chrome_height
    page.window.update()


ft.run(main)
