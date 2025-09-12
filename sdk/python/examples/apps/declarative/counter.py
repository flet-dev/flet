from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class AppState:
    count: int

    def increment(self):
        self.count += 1


@ft.component
def App():
    state, _ = ft.use_state(AppState(count=0))

    return ft.View(
        floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=state.increment
        ),
        controls=[
            ft.SafeArea(
                ft.Container(
                    ft.Text(value=f"{state.count}", size=50),
                    alignment=ft.Alignment.CENTER,
                ),
                expand=True,
            )
        ],
    )


ft.run(lambda page: page.render_views(App))
