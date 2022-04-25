import logging

import flet
from flet import (
    Checkbox,
    Column,
    ElevatedButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    icons,
)

logging.basicConfig(level=logging.DEBUG)


class Task:
    def __init__(self, app, name):
        self.app = app
        self.display_task = Checkbox(
            value=False, label=name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)
        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.EDIT,
                            tooltip="Edit todo",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE,
                            tooltip="Delete todo",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                ElevatedButton(text="Save", on_click=self.save_clicked),
            ],
        )
        self.view = Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.view.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.view.update()

    def delete_clicked(self, e):
        self.app.delete_task(self)

    def status_changed(self, e):
        self.app.update()


class TodoApp:
    def __init__(self):
        self.tasks = []
        self.new_task = TextField(hint_text="Whats needs to be done?", expand=1)
        self.tasks_view = Column()
        self.filter = Tabs(
            value="all",
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
        )
        self.items_left = Text("0 items left")
        self.view = Column(
            width=600,
            controls=[
                Row([Text(value="Todos", size=30)], alignment="center"),
                Row(
                    # on_submit=self.add_clicked,
                    controls=[
                        self.new_task,
                        ElevatedButton(text="Add", on_click=self.add_clicked),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks_view,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="Clear completed", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def update(self):
        status = self.filter.value
        count = 0
        for task in self.tasks:
            task.view.visible = (
                status == "all"
                or (status == "active" and task.display_task.value == False)
                or (status == "completed" and task.display_task.value)
            )
            if task.display_task.value == False:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        print("add before update111")
        self.view.update()

    def add_clicked(self, e):
        task = Task(self, self.new_task.value)
        self.tasks.append(task)
        self.tasks_view.controls.append(task.view)
        self.new_task.value = ""
        self.update()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.tasks_view.controls.remove(task.view)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks[:]:
            if task.display_task.value == True:
                self.delete_task(task)


def main(page: Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.update()
    app = TodoApp()
    page.add(app.view)


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
