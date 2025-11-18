import logging
from dataclasses import dataclass, field

import flet as ft

logging.basicConfig(level=logging.INFO)
logging.getLogger("flet_object_patch").setLevel(logging.INFO)
logging.getLogger("flet_components").setLevel(logging.INFO)

ItemID = ft.IdCounter()


@ft.observable
@dataclass
class AppState:
    groups: list["Group"] = field(default_factory=list)

    def move_group(self, src: "Group", dst: "Group"):
        src_index = self.groups.index(src)
        dst_index = self.groups.index(dst)
        if src_index != dst_index:
            print("Move group", src.title, "to position of", dst.title)
            self.groups.insert(dst_index, self.groups.pop(src_index))


@ft.observable
@dataclass
class Group:
    title: str
    color: ft.Colors
    items: list["Item"] = field(default_factory=list)

    def add_item(self, text: str):
        self.items.append(Item(text=text, group=self))

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
    id: int = field(default_factory=ItemID)

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
def ItemView(item: Item, **kwargs):
    is_item_over, set_is_item_over = ft.use_state(False)

    def on_accept(e: ft.DragTargetEvent):
        item.move_item_at(e.src.data, item)
        set_is_item_over(False)

    return ft.Column(
        spacing=2,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Divider(
                color=ft.Colors.BLACK38,
                thickness=2,
                height=2,
                radius=2,
                opacity=1.0 if is_item_over else 0.0,
            ),
            ft.Draggable(
                group="items",
                data=item,
                content=ft.DragTarget(
                    group="items",
                    data=item,
                    on_will_accept=lambda e: set_is_item_over(
                        e.accept and e.src.data != item
                    ),
                    on_accept=on_accept,
                    on_leave=lambda: set_is_item_over(False),
                    content=ft.Card(
                        content=ft.Container(
                            padding=7,
                            width=200,
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
def GroupView(group: Group, move_group, **kwargs):
    is_group_over, set_is_group_over = ft.use_state(False)
    is_item_over, set_is_item_over = ft.use_state(False)
    new_item_text, set_new_item_text = ft.use_state("")

    def on_item_accept(e: ft.DragTargetEvent):
        group.move_item_into(e.src.data)
        set_is_item_over(False)

    def on_group_accept(e: ft.DragTargetEvent):
        move_group(e.src.data, group)
        set_is_group_over(False)

    def on_add_item(self):
        if stripped_text := new_item_text.strip():
            group.add_item(stripped_text)
            set_new_item_text("")

    return ft.Row(
        spacing=4,
        intrinsic_height=True,
        controls=[
            ft.VerticalDivider(
                color=ft.Colors.BLACK_54,
                width=2,
                thickness=2,
                radius=2,
                leading_indent=15,
                trailing_indent=15,
                opacity=1.0 if is_group_over else 0.0,
            ),
            ft.Draggable(
                group="groups",
                data=group,
                content=ft.DragTarget(
                    group="items",
                    data=group,
                    on_will_accept=lambda e: set_is_item_over(e.accept),
                    on_accept=on_item_accept,
                    on_leave=lambda: set_is_item_over(False),
                    content=ft.DragTarget(
                        group="groups",
                        data=group,
                        on_will_accept=lambda e: set_is_group_over(
                            e.accept and e.src.data != group
                        ),
                        on_accept=on_group_accept,
                        on_leave=lambda: set_is_group_over(False),
                        content=ft.Container(
                            border=ft.Border.all(2, ft.Colors.BLACK12)
                            if not is_group_over
                            else ft.Border.all(2, ft.Colors.BLACK38),
                            border_radius=ft.BorderRadius.all(15),
                            bgcolor=group.color,
                            padding=ft.Padding.all(20),
                            width=220,
                            content=ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        group.title,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                    ),
                                    ft.TextField(
                                        label="New item",
                                        bgcolor=ft.Colors.WHITE,
                                        value=new_item_text,
                                        on_change=lambda e: set_new_item_text(
                                            e.control.value
                                        ),
                                        on_submit=on_add_item,
                                    ),
                                    ft.TextButton(
                                        content="Add",
                                        icon=ft.Icons.ADD,
                                        on_click=on_add_item,
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            *[
                                                ItemView(item, key=item.id)
                                                for item in group.items
                                            ],
                                            ft.Divider(
                                                color=ft.Colors.BLACK38,
                                                thickness=2,
                                                height=2,
                                                radius=2,
                                                opacity=1.0 if is_item_over else 0.0,
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

    # group_4 = Group(title="Group 4", color=ft.Colors.GREEN_400)
    # group_4.add_item("Item 5")

    app, _ = ft.use_state(
        lambda: AppState(
            groups=[
                group_1,
                group_2,
                group_3,
                # group_4,
            ]
        )
    )

    def on_mounted():
        ft.context.page.theme_mode = ft.ThemeMode.LIGHT

    ft.on_mounted(on_mounted)

    return ft.Row(
        spacing=4,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            GroupView(group, move_group=app.move_group, key=group.title)
            for group in app.groups
        ],
    )


ft.run(lambda page: page.render(App))
