import asyncio
import time
from dataclasses import dataclass

import flet as ft


def format_hhmmss(seconds: int) -> str:
    """Format elapsed seconds as HH:MM:SS."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


@ft.observable
@dataclass
class TimerState:
    running: bool = False
    paused: bool = False
    elapsed: int = 0

    _base_elapsed: int = 0
    _started_at: float = 0.0
    _task: asyncio.Task | None = None

    async def _ticker(self):
        while self.running:
            if not self.paused:
                self.elapsed = self._base_elapsed + int(time.time() - self._started_at)
            await asyncio.sleep(1)
        self._task = None

    def toggle(self):
        if not self.running:
            self.running = True
            self.paused = False
            self._base_elapsed = self.elapsed
            self._started_at = time.time()
            if self._task is None or self._task.done():
                self._task = asyncio.create_task(self._ticker())
            return

        if not self.paused:
            self._base_elapsed += int(time.time() - self._started_at)
            self.elapsed = self._base_elapsed
            self.paused = True
            return

        self.paused = False
        self._started_at = time.time()

    def stop(self):
        self.running = False
        self.paused = False
        self.elapsed = 0
        self._base_elapsed = 0
        self._started_at = 0.0


@ft.component
def App():
    state, _ = ft.use_state(TimerState())

    label = "Pause" if state.running and not state.paused else "Start"
    icon = ft.Icons.PAUSE if state.running and not state.paused else ft.Icons.PLAY_ARROW

    return ft.SafeArea(
        content=ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    format_hhmmss(state.elapsed),
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.FilledButton(
                            label,
                            icon=icon,
                            on_click=state.toggle,
                        ),
                        ft.TextButton(
                            "Stop",
                            icon=ft.Icons.STOP,
                            on_click=state.stop,
                            disabled=not state.running and state.elapsed == 0,
                        ),
                    ],
                ),
            ],
        )
    )


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
