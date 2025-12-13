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
    """
    Declarative timer state.

    This class is the single source of truth for the UI.
    Any mutation of its public fields automatically triggers a re-render.
    """

    running: bool = False
    paused: bool = False
    elapsed: int = 0  # seconds shown in UI

    # Internals
    _base_elapsed: int = 0  # accumulated time before the current run
    _started_at: float = 0.0  # wall-clock start time
    _task: asyncio.Task | None = None  # background ticker task

    async def _ticker(self):
        """
        Background task that updates elapsed time once per second
        while the timer is running.
        """
        while self.running:
            if not self.paused:
                self.elapsed = self._base_elapsed + int(time.time() - self._started_at)
            await asyncio.sleep(1)

        # Task cleanup when stopped
        self._task = None

    def toggle(self):
        """
        Toggle button handler:
        - stopped → start
        - running → pause
        - paused → resume
        """
        # stopped → start
        if not self.running:
            self.running = True
            self.paused = False
            self._base_elapsed = self.elapsed
            self._started_at = time.time()

            # Ensure only one ticker task runs
            if self._task is None or self._task.done():
                self._task = asyncio.create_task(self._ticker())
            return

        # running → pause
        if not self.paused:
            self._base_elapsed += int(time.time() - self._started_at)
            self.elapsed = self._base_elapsed
            self.paused = True
            return

        # paused → resume
        self.paused = False
        self._started_at = time.time()

    def stop(self):
        """Stop the timer and reset all state."""
        self.running = False
        self.paused = False
        self.elapsed = 0
        self._base_elapsed = 0
        self._started_at = 0.0


@ft.component
def App():
    state, _ = ft.use_state(TimerState())

    # Button appearance derived entirely from state
    label = "Pause" if state.running and not state.paused else "Start"
    icon = ft.Icons.PAUSE if state.running and not state.paused else ft.Icons.PLAY_ARROW

    return ft.SafeArea(
        ft.Column(
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
    """Application entry point."""
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.render(App)


ft.run(main)
