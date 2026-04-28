import asyncio
import time

import flet as ft


def main(page: ft.Page):
    page.title = "7GUIs - Timer"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    duration_seconds = 15.0
    elapsed_seconds = 0.0
    last_tick = time.monotonic()

    def refresh_ui():
        progress.value = (
            0 if duration_seconds == 0 else elapsed_seconds / duration_seconds
        )
        elapsed_label.value = f"{elapsed_seconds:0.1f}s elapsed"
        duration_label.value = f"Duration: {duration_seconds:0.1f}s"
        page.update()

    async def ticker():
        nonlocal elapsed_seconds, last_tick
        while True:
            await asyncio.sleep(0.1)
            now = time.monotonic()
            delta = now - last_tick
            last_tick = now
            if elapsed_seconds < duration_seconds:
                elapsed_seconds = min(duration_seconds, elapsed_seconds + delta)
                refresh_ui()

    def handle_duration_change(e: ft.Event[ft.Slider]):
        nonlocal duration_seconds, elapsed_seconds
        duration_seconds = round(float(e.control.value), 1)
        elapsed_seconds = min(elapsed_seconds, duration_seconds)
        refresh_ui()

    def reset(e: ft.Event[ft.TextButton]):
        nonlocal elapsed_seconds, last_tick
        elapsed_seconds = 0.0
        last_tick = time.monotonic()
        refresh_ui()

    page.add(
        ft.SafeArea(
            content=ft.Container(
                width=500,
                padding=28,
                border_radius=24,
                bgcolor=ft.Colors.TEAL_50,
                content=ft.Column(
                    tight=True,
                    spacing=18,
                    controls=[
                        ft.Text("Timer", size=28, weight=ft.FontWeight.W_700),
                        ft.Text(
                            "The timer starts immediately, fills the bar, and can be reset or resized.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        elapsed_label := ft.Text(size=34, weight=ft.FontWeight.W_600),
                        progress := ft.ProgressBar(
                            width=420,
                            value=0,
                            bar_height=16,
                            border_radius=12,
                            color=ft.Colors.TEAL_500,
                            bgcolor=ft.Colors.TEAL_50,
                        ),
                        duration_label := ft.Text(color=ft.Colors.BLUE_GREY_700),
                        ft.Slider(
                            min=1,
                            max=30,
                            divisions=58,
                            round=1,
                            value=duration_seconds,
                            label="{value}s",
                            on_change=handle_duration_change,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.TextButton(
                                    "Reset timer",
                                    icon=ft.Icons.RESTART_ALT,
                                    on_click=reset,
                                )
                            ],
                        ),
                    ],
                ),
            )
        )
    )
    refresh_ui()
    page.run_task(ticker)


if __name__ == "__main__":
    ft.run(main)
