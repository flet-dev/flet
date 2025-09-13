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
        dst.set_is_group_over(False)
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

    def set_is_item_over(self, value: bool):
        self.is_item_over = value

    def set_is_group_over(self, value: bool):
        self.is_group_over = value

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
        self.set_is_item_over(False)
        item.group.items.remove(item)
        item.group = self
        self.items.append(item)


@ft.observable
@dataclass
class Item:
    text: str
    group: Group
    is_item_over: bool = False

    def set_is_item_over(self, value: bool):
        self.is_item_over = value

    def move_item_at(self, item: "Item", to_item: "Item"):
        if item == to_item:
            return
        print(
            f"Move item {item.text} from {item.group.title} "
            f"to {to_item.group.title} at position of {to_item.text}"
        )
        self.set_is_item_over(False)
        item.group.items.remove(item)
        item.group = to_item.group
        to_index = to_item.group.items.index(to_item)
        to_item.group.items.insert(to_index, item)


@ft.component
def ItemView(item: Item):
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
                    on_will_accept=lambda e: item.set_is_item_over(
                        e.accept and e.src.data != item
                    ),
                    on_accept=lambda e: item.move_item_at(e.src.data, item),
                    on_leave=lambda: item.set_is_item_over(False),
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
                    on_will_accept=lambda e: group.set_is_item_over(e.accept),
                    on_accept=lambda e: group.move_item_into(e.src.data),
                    on_leave=lambda: group.set_is_item_over(False),
                    content=ft.DragTarget(
                        group="groups",
                        data=group,
                        on_will_accept=lambda e: group.set_is_group_over(
                            e.accept and e.src.data != group
                        ),
                        on_accept=lambda e: move_group(e.src.data, group),
                        on_leave=lambda: group.set_is_group_over(False),
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
