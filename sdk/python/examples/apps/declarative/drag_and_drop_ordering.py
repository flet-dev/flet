import logging
from dataclasses import dataclass, field

import flet as ft

logging.basicConfig(level=logging.INFO)
logging.getLogger("flet_components").setLevel(logging.INFO)


@ft.observable
@dataclass
class AppState:
    groups: list["Group"] = field(default_factory=list)


@ft.observable
@dataclass
class Group:
    title: str
    color: ft.Colors
    items: list["Item"] = field(default_factory=list)
    new_item_text: str = ""
    is_group_over: bool = False
    is_item_over: bool = False

    def add_item(self, text: str):
        self.items.append(Item(text=text, group=self))

    def change_new_item_text(self, new_item_text: str):
        self.new_item_text = new_item_text

    def on_add_item(self):
        if stripped_text := self.new_item_text.strip():
            self.add_item(stripped_text)
            self.new_item_text = ""


@ft.observable
@dataclass
class Item:
    text: str
    group: Group
    is_item_over: bool = False


@ft.component
def ItemView(item: Item):
    def on_will_accept(e: ft.DragWillAcceptEvent):
        item.is_item_over = e.accept and e.src.data != item
        if item.is_item_over:
            print("on_will_accept", item.text)

    def on_accept(e: ft.DragTargetEvent):
        item.is_item_over = False

    def on_leave(e: ft.DragTargetLeaveEvent):
        item.is_item_over = False

    return ft.Column(
        spacing=2,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLACK38,
                border_radius=ft.border_radius.all(30),
                height=2,
                width=180,
                opacity=1.0 if item.is_item_over else 0.0,
            ),
            ft.Draggable(
                group="items",
                data=item,
                content=ft.DragTarget(
                    group="items",
                    data=item,
                    on_will_accept=on_will_accept,
                    on_accept=on_accept,
                    on_leave=on_leave,
                    content=ft.Card(
                        elevation=1,
                        content=ft.Container(
                            width=200,
                            padding=7,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.START,
                                controls=[
                                    ft.Icon(ft.Icons.CIRCLE_OUTLINED),
                                    ft.Text(value=item.text),
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ],
    )


@ft.component
def GroupView(group: Group):
    def on_group_will_accept(e: ft.DragWillAcceptEvent):
        group.is_group_over = e.accept and e.src.data != group
        if group.is_group_over:
            print("on_group_will_accept", group.title)

    def on_group_accept(e: ft.DragTargetEvent):
        group.is_group_over = False

    def on_group_leave(e: ft.DragTargetLeaveEvent):
        group.is_group_over = False

    def on_item_will_accept(e: ft.DragWillAcceptEvent):
        group.is_item_over = e.accept and e.src.data.group != group
        if group.is_item_over:
            print("on_item_will_accept", group.title)

    def on_item_accept(e: ft.DragTargetEvent):
        group.is_item_over = False

    def on_item_leave(e: ft.DragTargetLeaveEvent):
        group.is_item_over = False

    return ft.Row(
        spacing=4,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLACK54,
                border_radius=ft.border_radius.all(30),
                width=2,
                height=100,
                opacity=1.0 if group.is_group_over else 0.0,
            ),
            ft.Draggable(
                group="groups",
                data=group,
                content=ft.DragTarget(
                    group="items",
                    data=group,
                    on_will_accept=on_item_will_accept,
                    on_accept=on_item_accept,
                    on_leave=on_item_leave,
                    content=ft.DragTarget(
                        group="groups",
                        data=group,
                        on_will_accept=on_group_will_accept,
                        on_accept=on_group_accept,
                        on_leave=on_group_leave,
                        content=ft.Container(
                            border=ft.Border.all(2, ft.Colors.BLACK12)
                            if not group.is_group_over
                            else ft.Border.all(2, ft.Colors.BLACK38),
                            border_radius=ft.BorderRadius.all(15),
                            bgcolor=group.color,
                            padding=ft.Padding.all(20),
                            content=ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        group.title,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                    ),
                                    ft.TextField(
                                        label="New item",
                                        width=200,
                                        bgcolor=ft.Colors.WHITE,
                                        value=group.new_item_text,
                                        on_change=lambda e: group.change_new_item_text(
                                            e.control.value
                                        ),
                                        on_submit=group.on_add_item,
                                    ),
                                    ft.TextButton(
                                        content="Add",
                                        icon=ft.Icons.ADD,
                                        on_click=group.on_add_item,
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            *[ItemView(item) for item in group.items],
                                            ft.Container(
                                                bgcolor=ft.Colors.BLACK38,
                                                border_radius=ft.border_radius.all(30),
                                                height=2,
                                                width=180,
                                                opacity=1.0
                                                if group.is_item_over
                                                else 0.0,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ],
    )


@ft.component
def App():
    group_1 = Group(title="List 1", color=ft.Colors.DEEP_ORANGE_400)
    group_1.add_item("Item 1")
    group_1.add_item("Item 2")

    group_2 = Group(title="List 2", color=ft.Colors.PINK_400)
    group_2.add_item("Item 3")

    group_3 = Group(title="List 3", color=ft.Colors.CYAN_400)
    group_3.add_item("Item 4")

    app, _ = ft.use_state(AppState(groups=[group_1, group_2, group_3]))

    return ft.Row(
        spacing=4,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[GroupView(group) for group in app.groups],
    )


ft.run(lambda page: page.render(App))
