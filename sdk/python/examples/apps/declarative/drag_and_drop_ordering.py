import logging
from dataclasses import dataclass, field

import flet as ft

logging.basicConfig(level=logging.INFO)
logging.getLogger("flet_components").setLevel(logging.INFO)


@ft.observable
@dataclass
class AppState:
    groups: list["Group"] = field(default_factory=list)

    def move_group(self, src: "Group", dst: "Group"):
        print("Move group", src.title, "to position of", dst.title)
        src_index = self.groups.index(src)
        dst_index = self.groups.index(dst)
        if src_index != dst_index:
            self.groups.insert(dst_index, self.groups.pop(src_index))


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

    def move_item_into(self, item: "Item"):
        print("Move item", item.text, "from", item.group.title, "to", self.title)
        item.group.items.remove(item)
        item.group = self
        self.items.append(item)


@ft.observable
@dataclass
class Item:
    text: str
    group: Group
    is_item_over: bool = False

    def move_item_at(self, item: "Item", to_item: "Item"):
        if item == to_item:
            return
        print(
            f"Move item {item.text} from {item.group.title} "
            f"to {to_item.group.title} at position of {to_item.text}"
        )
        item.group.items.remove(item)
        item.group = to_item.group
        to_index = to_item.group.items.index(to_item)
        to_item.group.items.insert(to_index, item)


@ft.component
def ItemView(item: Item):
    def on_will_accept(e: ft.DragWillAcceptEvent):
        item.is_item_over = e.accept and e.src.data != item

    def on_accept(e: ft.DragTargetEvent):
        item.move_item_at(e.src.data, item)
        item.is_item_over = False

    def on_leave(e: ft.DragTargetLeaveEvent):
        item.is_item_over = False

    return ft.Column(
        spacing=2,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLACK38,
                border_radius=ft.BorderRadius.all(30),
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
def GroupView(group: Group, move_group):
    def on_group_will_accept(e: ft.DragWillAcceptEvent):
        group.is_group_over = e.accept and e.src.data != group

    def on_group_accept(e: ft.DragTargetEvent):
        move_group(e.src.data, group)
        group.is_group_over = False

    def on_group_leave(e: ft.DragTargetLeaveEvent):
        group.is_group_over = False

    def on_item_will_accept(e: ft.DragWillAcceptEvent):
        group.is_item_over = e.accept

    def on_item_accept(e: ft.DragTargetEvent):
        group.move_item_into(e.src.data)
        group.is_item_over = False

    def on_item_leave(e: ft.DragTargetLeaveEvent):
        group.is_item_over = False

    return ft.Row(
        spacing=4,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLACK54,
                border_radius=ft.BorderRadius.all(30),
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
                                                border_radius=ft.BorderRadius.all(30),
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
    group_1 = Group(title="Group 1", color=ft.Colors.DEEP_ORANGE_400)
    group_1.add_item("Item 1")
    group_1.add_item("Item 2")

    group_2 = Group(title="Group 2", color=ft.Colors.PINK_400)
    group_2.add_item("Item 3")

    group_3 = Group(title="Group 3", color=ft.Colors.CYAN_400)
    group_3.add_item("Item 4")

    app, _ = ft.use_state(AppState(groups=[group_1, group_2, group_3]))

    return ft.Row(
        spacing=4,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[GroupView(group, move_group=app.move_group) for group in app.groups],
    )


ft.run(lambda page: page.render(App))
