import flet as ft


def main(page: ft.Page):
    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        page.update()

    new_task = ft.TextField(hint_text="Say hello?")
    test = ft.DatePicker()
    column = ft.Column(controls=[
        new_task,
        test
    ])

    page.add(column, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))


ft.app(target=main, view=ft.FLET_APP_HIDDEN, port=8550)
# ft.app(target=main, view=ft.FLET_APP_HIDDEN)
