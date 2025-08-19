from dataclasses import dataclass

import flet as ft


@dataclass
class AppState:
    count: int

    def increment(self):
        self.count += 1


def main(page: ft.Page):
    state = AppState(count=0)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=state.increment
    )
    page.add(
        ft.StateView(
            state,
            lambda state: ft.SafeArea(
                ft.Container(
                    ft.Text(value=f"{state.count}", size=50),
                    alignment=ft.Alignment.CENTER,
                ),
                expand=True,
            ),
            expand=True,
        )
    )


ft.run(main)
