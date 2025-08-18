import itertools
from dataclasses import dataclass, field
from typing import cast

import flet as ft

task_id = itertools.count(1)


@dataclass
class TaskItem:
    name: str
    completed: bool = False
    edit_mode: bool = False
    new_name: str = ""
    id: int = field(default_factory=lambda: next(task_id))

    def toggle_task_status(self):
        self.completed = not self.completed

    def edit(self):
        self.new_name = self.name
        self.edit_mode = True

    def set_new_name(self, new_name: str):
        self.new_name = new_name

    def complete_edit(self):
        self.name = self.new_name
        self.edit_mode = False


@dataclass
class TodoAppState:
    tasks: list[TaskItem] = field(default_factory=list)
    statuses: list[str] = field(default_factory=lambda: ["all", "active", "completed"])
    status: str = "all"
    new_task_field: ft.Ref = field(default_factory=lambda: ft.Ref())
    new_task_name: str = ""

    def get_tasks(self) -> list[TaskItem]:
        return list(
            filter(
                lambda task: self.status == "all"
                or self.status == "active"
                and not task.completed
                or self.status == "completed"
                and task.completed,
                self.tasks,
            )
        )

    @property
    def active_tasks_number(self) -> int:
        return len([task for task in self.tasks if not task.completed])

    def status_changed(self, e: ft.Event[ft.Tabs]):
        self.status = self.statuses[e.control.selected_index]

    def set_new_task_name(self, e: ft.Event[ft.TextField]):
        self.new_task_name = e.control.value

    async def add_task(self):
        self.tasks.append(TaskItem(self.new_task_name))
        self.new_task_name = ""
        await cast(ft.TextField, self.new_task_field.current).focus()

    def delete_task(self, task: TaskItem):
        self.tasks.remove(task)

    def clear_completed(self):
        self.tasks = list(filter(lambda task: not task.completed, self.tasks))


def TodoAppView(state: TodoAppState):
    return ft.Column(
        [
            Header(),
            ft.Row(
                controls=[
                    ft.TextField(
                        ref=state.new_task_field,
                        hint_text="What needs to be done?",
                        on_submit=state.add_task,
                        value=state.new_task_name,
                        on_change=state.set_new_task_name,
                        autofocus=True,
                        expand=True,
                    ),
                    ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=state.add_task),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    ft.Tabs(
                        selected_index=state.statuses.index(state.status),
                        length=len(state.statuses),
                        on_change=state.status_changed,
                        content=ft.TabBar(
                            scrollable=False,
                            tabs=[ft.Tab(label=tab) for tab in state.statuses],
                        ),
                    ),
                    ft.Column(
                        [TaskItemView(state, task) for task in state.get_tasks()]
                    ),
                    Footer(state),
                ],
            ),
        ]
    )


def TaskItemView(state: TodoAppState, task: TaskItem):
    return (
        ft.Row(
            key=task.id,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Checkbox(
                    value=task.completed,
                    label=task.name,
                    on_change=lambda: task.toggle_task_status(),
                ),
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=lambda: task.edit(),
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=lambda: state.delete_task(task),
                        ),
                    ],
                ),
            ],
        )
        if not task.edit_mode
        else ft.Row(
            key=task.id,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.TextField(
                    value=task.new_name,
                    on_change=lambda e: task.set_new_name(e.control.value),
                    expand=1,
                ),
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=lambda: task.complete_edit(),
                ),
            ],
        )
    )


def Header():
    return ft.Row(
        [
            ft.Text(
                value="Todos",
                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )


def Footer(state: TodoAppState):
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(f"{state.active_tasks_number} items left"),
            ft.OutlinedButton(
                content="Clear completed",
                on_click=state.clear_completed,
            ),
        ],
    )


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO

    state = TodoAppState()
    page.add(ft.StateView(state, lambda state: TodoAppView(state)))


ft.run(main)
