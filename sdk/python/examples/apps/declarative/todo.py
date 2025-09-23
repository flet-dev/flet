import logging
from dataclasses import dataclass, field
from typing import cast

import flet as ft

logging.basicConfig(level=logging.INFO)

TaskID = ft.IdCounter()


@ft.observable
@dataclass
class TaskItem:
    name: str
    completed: bool = False
    id: int = field(default_factory=TaskID)

    def update_task(self, new_name: str):
        self.name = new_name

    def toggle_task_status(self):
        self.completed = not self.completed


@ft.observable
@dataclass
class TodoAppState:
    tasks: list[TaskItem] = field(default_factory=list)
    statuses: list[str] = field(default_factory=lambda: ["all", "active", "completed"])
    status: str = "all"

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

    def add_task(self, new_task_event: str):
        self.tasks.append(TaskItem(new_task_event))

    def delete_task(self, task: TaskItem):
        self.tasks.remove(task)

    def clear_completed(self):
        self.tasks = list(filter(lambda task: not task.completed, self.tasks))


@ft.component
def TodoAppView():
    state, _ = ft.use_state(lambda: TodoAppState())
    new_task_name, set_new_task_name = ft.use_state("")
    new_task_field: ft.Ref = ft.Ref()

    async def add_task():
        state.add_task(new_task_name)
        set_new_task_name("")
        await cast(ft.TextField, new_task_field.current).focus()

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column(
                [
                    Header(),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                ref=new_task_field,
                                hint_text="What needs to be done?",
                                on_submit=add_task,
                                value=new_task_name,
                                on_change=lambda e: set_new_task_name(e.control.value),
                                autofocus=True,
                                expand=True,
                            ),
                            ft.FloatingActionButton(
                                icon=ft.Icons.ADD,
                                on_click=add_task,
                            ),
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
                                [
                                    TaskItemView(task, state.delete_task, key=task.id)
                                    for task in state.get_tasks()
                                ]
                            ),
                            Footer(
                                active_tasks_number=state.active_tasks_number,
                                clear_completed=state.clear_completed,
                            ),
                        ],
                    ),
                ]
            )
        ],
    )


@ft.component
def TaskItemView(task: TaskItem, delete_task, key=None) -> ft.Control:
    edit_mode, set_edit_mode = ft.use_state(False)
    new_name, set_new_name = ft.use_state("")

    def edit():
        set_edit_mode(True)
        set_new_name(task.name)

    def complete_edit():
        task.update_task(new_name)
        set_edit_mode(False)

    return (
        ft.Row(
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
                            on_click=edit,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=lambda: delete_task(task),
                        ),
                    ],
                ),
            ],
        )
        if not edit_mode
        else ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.TextField(
                    value=new_name,
                    on_change=lambda e: set_new_name(e.control.value),
                    expand=1,
                ),
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=complete_edit,
                ),
            ],
        )
    )


@ft.component
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


@ft.component
def Footer(active_tasks_number: int, clear_completed):
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(f"{active_tasks_number} items left"),
            ft.OutlinedButton(
                content="Clear completed",
                on_click=clear_completed,
            ),
        ],
    )


ft.run(lambda page: page.render_views(TodoAppView))
