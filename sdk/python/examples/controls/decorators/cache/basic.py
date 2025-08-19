import logging
from dataclasses import dataclass, field

import flet as ft

logging.basicConfig(level=logging.DEBUG)


@dataclass
class AppState:
    number: int = 0
    items: list[int] = field(default_factory=list)

    def __post_init__(self):
        for _ in range(10):
            self.add_item()

    def add_item(self):
        self.items.append(self.number)
        self.number += 1


@ft.cache
def item_view(i: int):
    return ft.Container(
        ft.Text(f"Item {i}"),
        padding=10,
        bgcolor=ft.Colors.AMBER_100,
        key=i,
    )


def main(page: ft.Page):
    state = AppState()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=state.add_item
    )
    page.add(
        ft.StateView(
            state,
            lambda state: ft.SafeArea(
                ft.Row([item_view(i) for i in state.items], wrap=True)
            ),
            expand=True,
        )
    )


ft.run(main)
