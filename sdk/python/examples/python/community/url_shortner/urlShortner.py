import flet as ft
import pyshorteners


def main(page: ft.Page):
    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter the url"
            page.update()
        else:
            name = txt_name.value
            s = pyshorteners.Shortener()
            # page.clean()
            page.add(ft.Text(f"Short link - {s.tinyurl.short(name)}"))

    txt_name = ft.TextField(label="Enter the url")

    page.add(txt_name, ft.ElevatedButton("Create URL!", on_click=btn_click))


ft.app(target=main)
# ft.app(target=main, view=ft.WEB_BROWSER)
