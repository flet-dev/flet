from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class Item:
    id: str
    label: str


@ft.observable
@dataclass
class AppState:
    items: list[Item]
    next_item_index: int = 0

    def add_items(self, items: Item | list[Item]):
        items_to_add = items if isinstance(items, list) else [items]
        self.items = self.items + items_to_add

    def add_new_item(self):
        item = Item(
            id=f"item-{self.next_item_index}",
            label=f"Item {self.next_item_index}",
        )
        self.next_item_index += 1
        self.add_items(item)

    def remove_items(self, items: Item | list[Item]):
        items_to_remove = items if isinstance(items, list) else [items]
        removal_set = set(items_to_remove)
        self.items = [item for item in self.items if item not in removal_set]

    def drag_reorder(self, e: ft.OnReorderEvent):
        if e.old_index is not None and e.new_index is not None:
            dragged_item = self.items.pop(e.old_index)
            self.items.insert(e.new_index, dragged_item)


@ft.component
def ItemView(item: Item, on_remove, allow_add_remove: bool = True) -> ft.Control:
    return ft.ListTile(
        leading=ft.ReorderableDragHandle(
            content=ft.Icon(ft.Icons.DRAG_INDICATOR, color=ft.Colors.RED),
            mouse_cursor=ft.MouseCursor.GRAB,
        ),
        width=300,
        bgcolor="#5E6063",
        title=ft.Row(
            controls=[
                ft.Container(
                    expand=True,
                    height=40,
                    bgcolor="#8DA6C6",
                    content=ft.Text(item.label),
                ),
                ft.Container(
                    visible=allow_add_remove,
                    on_click=lambda _: on_remove(item),
                    content=ft.Icon(
                        icon=ft.Icons.REMOVE,
                        color=ft.Colors.AMBER,
                    ),
                ),
            ]
        ),
    )


@ft.component
def App(items: list[Item] | None = None, allow_add_remove: bool = True):
    if items is None:
        items = [Item(id=f"item-{i}", label=f"Item {i}") for i in range(3)]

    state, _ = ft.use_state(
        lambda: AppState(items=list(items), next_item_index=len(items))
    )

    return ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.FilledButton(
                    content="Add item",
                    visible=allow_add_remove,
                    on_click=lambda _: state.add_new_item(),
                ),
                ft.ReorderableListView(
                    spacing=0,
                    show_default_drag_handles=False,
                    on_reorder=state.drag_reorder,
                    controls=[
                        ItemView(
                            item,
                            on_remove=state.remove_items,
                            allow_add_remove=allow_add_remove,
                            key=item.id,
                        )
                        for item in state.items
                    ],
                ),
            ]
        )
    )


def main(page: ft.Page):
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
