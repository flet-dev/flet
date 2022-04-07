import flet
from flet import Text, Stack, Textbox, Button, Checkbox, Tabs, Tab


class Task:
    def __init__(self, app, name):
        self.app = app
        self.display_task = Checkbox(
            value=False, label=name, on_change=self.status_changed
        )
        self.edit_name = Textbox(width="100%")
        self.display_view = Stack(
            horizontal=True,
            horizontal_align="space-between",
            vertical_align="center",
            controls=[
                self.display_task,
                Stack(
                    horizontal=True,
                    gap="0",
                    controls=[
                        Button(
                            icon="Edit", title="Edit todo", on_click=self.edit_clicked
                        ),
                        Button(
                            icon="Delete",
                            title="Delete todo",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        self.edit_view = Stack(
            visible=False,
            horizontal=True,
            horizontal_align="space-between",
            vertical_align="center",
            controls=[self.edit_name, Button(text="Save", on_click=self.save_clicked)],
        )
        self.view = Stack(controls=[self.display_view, self.edit_view])

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
        self.new_task = Textbox(placeholder="Whats needs to be done?", width="100%")
        self.tasks_view = Stack()
        self.filter = Tabs(
            value="all",
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
        )
        self.items_left = Text("0 items left")
        self.view = Stack(
            width="70%",
            controls=[
                Text(value="Todos", size="large", align="center"),
                Stack(
                    horizontal=True,
                    on_submit=self.add_clicked,
                    controls=[
                        self.new_task,
                        Button(primary=True, text="Add", on_click=self.add_clicked),
                    ],
                ),
                Stack(
                    gap=25,
                    controls=[
                        self.filter,
                        self.tasks_view,
                        Stack(
                            horizontal=True,
                            horizontal_align="space-between",
                            vertical_align="center",
                            controls=[
                                self.items_left,
                                Button(
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


def main(page):
    page.title = "ToDo App"
    page.horizontal_align = "center"
    page.update()
    app = TodoApp()
    page.add(app.view)


flet.app("todo-app", target=main)
