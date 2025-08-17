import flet as ft


def example(page):
    class Task(ft.UserControl):
        def __init__(self, task_name, task_status_change, task_delete):
            super().__init__()
            self.completed = False
            self.task_name = task_name
            self.task_status_change = task_status_change
            self.task_delete = task_delete

        def build(self):
            self.display_task = ft.Checkbox(
                value=False, label=self.task_name, on_change=self.status_changed
            )
            self.edit_name = ft.TextField(expand=1)

            self.display_view = ft.Row(
                alignment="spaceBetween",
                vertical_alignment="center",
                controls=[
                    self.display_task,
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.CREATE_OUTLINED,
                                tooltip="Edit To-Do",
                                on_click=self.edit_clicked,
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                tooltip="Delete To-Do",
                                on_click=self.delete_clicked,
                            ),
                        ],
                    ),
                ],
            )

            self.edit_view = ft.Row(
                visible=False,
                alignment="spaceBetween",
                vertical_alignment="center",
                controls=[
                    self.edit_name,
                    ft.IconButton(
                        icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.Colors.GREEN,
                        tooltip="Update To-Do",
                        on_click=self.save_clicked,
                    ),
                ],
            )
            return ft.Column(controls=[self.display_view, self.edit_view])

        def edit_clicked(self, e):
            self.edit_name.value = self.display_task.label
            self.display_view.visible = False
            self.edit_view.visible = True
            self.update()

        def save_clicked(self, e):
            self.display_task.label = self.edit_name.value
            self.display_view.visible = True
            self.edit_view.visible = False
            self.update()

        def status_changed(self, e):
            self.completed = self.display_task.value
            self.task_status_change(self)

        def delete_clicked(self, e):
            self.task_delete(self)

    class TodoApp(ft.UserControl):
        def build(self):
            self.expand = True
            self.new_task = ft.TextField(
                hint_text="What needs to be done?",
                on_submit=self.add_clicked,
                expand=True,
            )
            self.tasks = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

            self.filter = ft.TabBar(
                scrollable=False,
                tabs=[
                    ft.Tab(label="all"),
                    ft.Tab(label="active"),
                    ft.Tab(label="completed"),
                ],
            )

            self.filter_tabs = ft.Tabs(
                length=3,
                selected_index=0,
                on_change=lambda e: self.update(),
                content=self.filter,
            )

            self.items_left = ft.Text("0 items left")

            # application's root control (i.e. "view") containing all other controls
            return ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            self.new_task,
                            ft.FloatingActionButton(
                                icon=ft.Icons.ADD, on_click=self.add_clicked
                            ),
                        ],
                    ),
                    self.filter_tabs,
                    self.tasks,
                    ft.Row(
                        alignment="spaceBetween",
                        vertical_alignment="center",
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Clear completed",
                                on_click=self.clear_clicked,
                            ),
                        ],
                    ),
                ],
            )

        async def add_clicked(self, e):
            if self.new_task.value:
                task = Task(
                    self.new_task.value, self.task_status_change, self.task_delete
                )
                self.tasks.controls.append(task)
                self.new_task.value = ""
                await self.new_task.focus()
                self.update()

        def task_status_change(self, task):
            self.update()

        def task_delete(self, task):
            self.tasks.controls.remove(task)
            self.update()

        def tabs_changed(self, e):
            self.update()

        def clear_clicked(self, e):
            for task in self.tasks.controls[:]:
                if task.completed:
                    self.task_delete(task)

        def update(self):
            status = self.filter.tabs[self.filter_tabs.selected_index].label
            count = 0
            for task in self.tasks.controls:
                task.visible = (
                    status == "all"
                    or (status == "active" and not task.completed)
                    or (status == "completed" and task.completed)
                )
                if not task.completed:
                    count += 1
            self.items_left.value = f"{count} active item(s) left"
            super().update()

    app = TodoApp()
    return ft.SafeArea(app, expand=True)


def main(page: ft.Page):
    page.title = "Flet to_do example"
    page.window_width = 390
    page.window_height = 844
    page.add(
        ft.Row(
            [ft.Text(value="Todos", style="headlineMedium")],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        example(page),
    )


if __name__ == "__main__":
    ft.run(main)
