import asyncio
import time

import flet as ft


def format_hhmmss(seconds: int) -> str:
    """Convert elapsed seconds into HH:MM:SS string."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    running = False
    paused = False
    elapsed = 0
    base_elapsed = 0
    started_at = 0.0

    def sync_ui():
        nonlocal elapsed
        timer.value = format_hhmmss(elapsed)

        if running and not paused:
            toggle_btn.text = "Pause"
            toggle_btn.icon = ft.Icons.PAUSE
        else:
            toggle_btn.text = "Start"
            toggle_btn.icon = ft.Icons.PLAY_ARROW

        stop_btn.disabled = (not running) and (elapsed == 0)
        page.update()

    async def ticker():
        nonlocal elapsed
        while running:
            if not paused:
                elapsed = base_elapsed + int(time.time() - started_at)
                timer.value = format_hhmmss(elapsed)
                timer.update()
            await asyncio.sleep(1)

    def handle_toggle():
        nonlocal running, paused, elapsed, base_elapsed, started_at

        if not running:
            running = True
            paused = False
            base_elapsed = elapsed
            started_at = time.time()
            page.run_task(ticker)
            sync_ui()
            return

        if not paused:
            base_elapsed += int(time.time() - started_at)
            elapsed = base_elapsed
            paused = True
            sync_ui()
            return

        paused = False
        started_at = time.time()
        sync_ui()

    def handle_stop():
        nonlocal running, paused, elapsed, base_elapsed, started_at
        running = False
        paused = False
        elapsed = 0
        base_elapsed = 0
        started_at = 0.0
        sync_ui()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    timer := ft.Text("00:00:00", size=30, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            toggle_btn := ft.FilledButton(
                                "Start",
                                icon=ft.Icons.PLAY_ARROW,
                                on_click=handle_toggle,
                            ),
                            stop_btn := ft.TextButton(
                                "Stop",
                                icon=ft.Icons.STOP,
                                disabled=True,
                                on_click=handle_stop,
                            ),
                        ],
                    ),
                ],
            )
        )
    )

    sync_ui()


if __name__ == "__main__":
    ft.run(main)
