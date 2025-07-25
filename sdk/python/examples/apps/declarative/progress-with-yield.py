import asyncio
from dataclasses import dataclass

import flet as ft


@dataclass
class AppState:
    counter: float

    async def start_counter(self):
        self.counter = 0
        yield
        for _ in range(0, 10):
            self.counter += 0.1
            yield
            await asyncio.sleep(0.5)


def main(page: ft.Page):
    state = AppState(counter=0)

    page.add(
        ft.ControlBuilder(
            state,
            lambda state: ft.Column(
                [
                    ft.ProgressBar(state.counter),
                    ft.Button("Run!", on_click=state.start_counter),
                ]
            ),
        )
    )


ft.run(main)
