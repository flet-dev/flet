import flet as ft


def main(page: ft.Page):
    def add_clicked(e):
        page.add(ft.Checkbox(label=f"{new_task.value} - {test.value}"))
        new_task.value = ""
        page.update()

    new_task = ft.TextField(
        hint_text="Say hello?",
        on_change=add_clicked
    )
    test = ft.DateField(on_change=add_clicked)
    column = ft.Column(controls=[
        new_task,
        test
    ])

    page.add(column, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))


ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
# ft.app(target=main, view=ft.FLET_APP_HIDDEN)
