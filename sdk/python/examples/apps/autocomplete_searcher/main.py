from names import NAMES

import flet as ft


def printer(e):
    print("Yellow!")


def main(page: ft.Page):
    page.title = "Autocomplete search names"

    def textbox_changed(string):
        str_lower = string.control.value.lower()
        list_view.controls = (
            [list_items.get(n) for n in NAMES if str_lower in n.lower()]
            if str_lower
            else []
        )
        page.update()

    list_items = {
        name: ft.ListTile(
            title=ft.Text(name),
            leading=ft.Icon(ft.Icons.ACCESSIBILITY),
            on_click=printer,
        )
        for name in NAMES
    }

    text_field = ft.TextField(label="Search name:", on_change=textbox_changed)
    list_view = ft.ListView(expand=1, spacing=10, padding=20)

    page.add(text_field, list_view)


ft.run(port=8080, target=main, view=ft.WEB_BROWSER)
