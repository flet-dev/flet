import flet
from flet import Checkbox, FloatingActionButton, Icons, Page, TextField


def main(page: Page):
    def add_clicked(e):
        page.add(Checkbox(label=new_task.value))
        new_task.value = ""
        page.update()

    new_task = TextField(hint_text="Whats needs to be done?")

    page.add(new_task, FloatingActionButton(icon=Icons.ADD, on_click=add_clicked))


flet.run(main)
