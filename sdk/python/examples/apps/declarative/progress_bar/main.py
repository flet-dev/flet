import asyncio
from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class AppState:
    counter: float

    async def start_counter(self):
        self.counter = 0
        for _ in range(0, 10):
            self.counter += 0.1
            await asyncio.sleep(0.5)


@ft.component
def App():
    state, _ = ft.use_state(AppState(counter=0))

    return ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.ProgressBar(state.counter),
                ft.Button("Run!", on_click=state.start_counter),
            ]
        )
    )


def main(page: ft.Page):
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
