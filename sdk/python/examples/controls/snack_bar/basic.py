import flet as ft


def main(page: ft.Page):
    def on_click(e: ft.Event[ft.Button]):
        page.show_dialog(ft.SnackBar(ft.Text("Hello, world!")))

    page.add(ft.Button("Open SnackBar", on_click=on_click))


ft.run(main)
