import flet as ft


def main(page: ft.Page):
    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        page.update()

    new_task = ft.TextField(hint_text="Say hello?")

    page.add(new_task, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))


ft.app(target=main, view=ft.FLET_APP, port=8085)
# ft.app(target=main, view=ft.FLET_APP_HIDDEN)
