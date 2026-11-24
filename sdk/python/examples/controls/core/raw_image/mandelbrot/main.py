import asyncio
import time
from collections import deque

import numpy as np

import flet as ft

WIDTH = 640
HEIGHT = 480
MAX_ITER = 96
ZOOM_PER_CLICK = 8.0
ZOOM_FRAMES = 30
HOME = (-0.65, 0.0, 1.6)  # center x, center y, half-width of the view
FPS_WINDOW_SECONDS = 2.0


def mandelbrot_frame(center_x: float, center_y: float, scale: float) -> np.ndarray:
    """
    Escape-time Mandelbrot render, fully vectorized: points that stay
    bounded for MAX_ITER iterations are painted black, escaped points get
    a sine palette keyed on the escape iteration.
    """
    aspect = HEIGHT / WIDTH
    x = np.linspace(center_x - scale, center_x + scale, WIDTH)
    y = np.linspace(center_y - scale * aspect, center_y + scale * aspect, HEIGHT)
    c = x[None, :] + 1j * y[:, None]
    z = np.zeros_like(c)
    escape_iter = np.full(c.shape, MAX_ITER, dtype=np.int32)
    alive = np.ones(c.shape, dtype=bool)
    for i in range(MAX_ITER):
        z[alive] = z[alive] ** 2 + c[alive]
        escaped = alive & (np.abs(z) > 2.0)
        escape_iter[escaped] = i
        alive &= ~escaped
    t = escape_iter / MAX_ITER
    frame = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    outside = ~alive
    frame[outside, 0] = np.sin(t[outside] * 9.0) * 127 + 128
    frame[outside, 1] = np.sin(t[outside] * 9.0 + 1.2) * 127 + 128
    frame[outside, 2] = np.sin(t[outside] * 9.0 + 2.4) * 127 + 128
    frame[..., 3] = 255
    return frame


async def main(page: ft.Page):
    page.title = "RawImage Mandelbrot"

    # No fixed size: the control fills the window (expand=True) and CONTAIN
    # scales the 640x480 frame into whatever box the layout provides, so the
    # image grows and shrinks with the window.
    raw_image = ft.RawImage(expand=True, fit=ft.BoxFit.CONTAIN)
    fps_text = ft.Text("fps: —", size=12)
    zoom_text = ft.Text("zoom: 1x", size=12)
    hint_text = ft.Text("click to zoom in", size=12, italic=True)

    view = HOME
    frame_times: deque[float] = deque()
    zoom_task: asyncio.Task | None = None
    box_size = (float(WIDTH), float(HEIGHT))  # laid-out size of the control

    def track_size(e: ft.LayoutSizeChangeEvent):
        nonlocal box_size
        box_size = (e.width, e.height)

    raw_image.on_size_change = track_size

    async def show(center_x: float, center_y: float, scale: float):
        nonlocal view
        view = (center_x, center_y, scale)
        # The render itself is CPU-heavy — keep it off the event loop.
        frame = await asyncio.to_thread(mandelbrot_frame, center_x, center_y, scale)
        await raw_image.render(frame, premultiplied=True)
        now = time.monotonic()
        frame_times.append(now)
        while frame_times and frame_times[0] < now - FPS_WINDOW_SECONDS:
            frame_times.popleft()
        fps_text.value = f"fps: {len(frame_times) / FPS_WINDOW_SECONDS:.1f}"
        zoom_text.value = f"zoom: {HOME[2] / scale:,.0f}x"
        page.update()

    async def zoom_to(target_x: float, target_y: float, factor: float):
        # A burst of ZOOM_FRAMES awaited renders: exponential interpolation
        # of the view towards the target, each frame displayed as soon as
        # the client acks the previous one.
        start_x, start_y, start_scale = view
        for i in range(1, ZOOM_FRAMES + 1):
            k = i / ZOOM_FRAMES
            f = factor**k
            scale = start_scale / f
            x = target_x + (start_x - target_x) / f
            y = target_y + (start_y - target_y) / f
            try:
                await show(x, y, scale)
            except (RuntimeError, TimeoutError):
                return

    def start_zoom(target_x: float, target_y: float, factor: float):
        nonlocal zoom_task
        if zoom_task is not None and not zoom_task.done():
            return  # ignore clicks while a zoom animation is running
        zoom_task = asyncio.create_task(zoom_to(target_x, target_y, factor))

    def tap(e: ft.TapEvent):
        if e.local_position is None:
            return
        # With CONTAIN the frame is centered in the box with letterbox
        # bands; undo that mapping to get frame-pixel coordinates.
        box_width, box_height = box_size
        display_scale = min(box_width / WIDTH, box_height / HEIGHT)
        offset_x = (box_width - WIDTH * display_scale) / 2
        offset_y = (box_height - HEIGHT * display_scale) / 2
        frame_x = (e.local_position.x - offset_x) / display_scale
        frame_y = (e.local_position.y - offset_y) / display_scale
        if not (0 <= frame_x < WIDTH and 0 <= frame_y < HEIGHT):
            return  # tap landed on a letterbox band
        center_x, center_y, scale = view
        aspect = HEIGHT / WIDTH
        x = center_x + (frame_x / WIDTH * 2 - 1) * scale
        y = center_y + (frame_y / HEIGHT * 2 - 1) * scale * aspect
        start_zoom(x, y, ZOOM_PER_CLICK)

    def reset():
        nonlocal zoom_task
        if zoom_task is not None:
            zoom_task.cancel()
            zoom_task = None
        asyncio.create_task(show(*HOME))

    page.add(
        ft.Row(
            [
                ft.OutlinedButton("Reset", on_click=reset),
                zoom_text,
                fps_text,
                hint_text,
            ],
            spacing=20,
        ),
        ft.GestureDetector(content=raw_image, on_tap_down=tap, expand=True),
    )

    await show(*HOME)


if __name__ == "__main__":
    ft.run(main)
