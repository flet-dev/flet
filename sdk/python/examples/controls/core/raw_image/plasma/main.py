import asyncio
import time
from collections import deque

import numpy as np

import flet as ft

FPS_WINDOW_SECONDS = 2.0


def plasma_frame(width: int, height: int, t: float) -> np.ndarray:
    """
    Renders a classic demoscene plasma: several drifting sine fields summed
    and mapped through a rotating RGB palette. Fully vectorized in numpy.
    """
    x = np.linspace(0.0, 3.0 * np.pi, width, dtype=np.float32)[None, :]
    y = np.linspace(0.0, 3.0 * np.pi, height, dtype=np.float32)[:, None]
    cx = x - 1.5 * np.pi + np.sin(t / 3.0) * np.pi
    cy = y - 1.5 * np.pi + np.cos(t / 2.0) * np.pi
    v = (
        np.sin(x + t)
        + np.sin((y + t) / 2.0)
        + np.sin((x + y + t) / 2.0)
        + np.sin(np.sqrt(cx * cx + cy * cy + 1.0) + t)
    ) / 4.0
    frame = np.empty((height, width, 4), dtype=np.uint8)
    frame[..., 0] = np.sin(v * np.pi) * 127 + 128
    frame[..., 1] = np.sin(v * np.pi + 2.0 * np.pi / 3.0) * 127 + 128
    frame[..., 2] = np.sin(v * np.pi + 4.0 * np.pi / 3.0) * 127 + 128
    frame[..., 3] = 255
    return frame


async def main(page: ft.Page):
    page.title = "RawImage plasma"
    page.padding = 0

    raw_image = ft.RawImage(expand=True, fit=ft.BoxFit.FILL)

    fps_text = ft.Text("fps: —", size=12)
    resolution_text = ft.Text("res: —", size=12)
    detail_slider = ft.Slider(
        min=1,
        max=8,
        divisions=7,
        value=2,
        width=200,
        label="downscale 1/{value}",
    )

    status_bar = ft.Container(
        content=ft.Row(
            [fps_text, resolution_text, ft.Text("detail:", size=12), detail_slider],
            spacing=20,
        ),
        padding=ft.Padding.symmetric(horizontal=12, vertical=2),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column([raw_image, status_bar], expand=True, spacing=0),
            expand=True,
        )
    )

    frame_times: deque[float] = deque()
    frame_size = (0, 0)

    async def animate():
        nonlocal frame_size
        started = time.monotonic()
        while True:
            downscale = int(detail_slider.value)
            width = max(2, int(page.width or 800) // downscale)
            height = max(2, (int(page.height or 600) - 50) // downscale)
            frame_size = (width, height)
            frame = plasma_frame(width, height, time.monotonic() - started)
            try:
                # The frame is opaque, so it is premultiplied by definition —
                # saying so skips an alpha scan per frame. The await resolves
                # when the frame is on screen, pacing the loop to display
                # speed.
                await raw_image.render(frame, premultiplied=True)
            except (RuntimeError, TimeoutError):
                return  # window closed — session destroyed
            now = time.monotonic()
            frame_times.append(now)
            while frame_times and frame_times[0] < now - FPS_WINDOW_SECONDS:
                frame_times.popleft()

    async def refresh_stats():
        # Refresh labels at ~4 Hz instead of once per frame, which would
        # thrash the layout.
        while True:
            now = time.monotonic()
            while frame_times and frame_times[0] < now - FPS_WINDOW_SECONDS:
                frame_times.popleft()
            fps_text.value = f"fps: {len(frame_times) / FPS_WINDOW_SECONDS:.1f}"
            resolution_text.value = f"res: {frame_size[0]}x{frame_size[1]}"
            try:
                page.update()
            except RuntimeError:
                return
            await asyncio.sleep(0.25)

    asyncio.create_task(animate())
    asyncio.create_task(refresh_stats())


if __name__ == "__main__":
    ft.run(main)
