import asyncio
import contextlib
import io
import random
import threading
import time
from typing import Optional

from PIL import Image, ImageDraw

import flet as ft
import flet.canvas as fc


# ---------- frame generator ----------
def make_frame(i: int, w: int = 640, h: int = 480) -> bytes:
    img = Image.new(
        "RGB",
        (w, h),
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    )
    draw = ImageDraw.Draw(img)

    # random circles
    for _ in range(10):
        x1, y1 = random.randint(0, w - 40), random.randint(0, h - 40)
        x2, y2 = x1 + random.randint(20, 80), y1 + random.randint(20, 80)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.ellipse([x1, y1, x2, y2], fill=color, outline="black")

    # random lines
    for _ in range(10):
        x1, y1 = random.randint(0, w - 1), random.randint(0, h - 1)
        x2, y2 = random.randint(0, w - 1), random.randint(0, h - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.line([x1, y1, x2, y2], fill=color, width=3)

    # label
    draw.text((10, 10), f"Frame {i}\n{time.strftime('%H:%M:%S')}", fill="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------- producer thread: pushes into asyncio.Queue ----------
def producer_thread(
    loop: asyncio.AbstractEventLoop,
    q: asyncio.Queue,
    stop_evt: threading.Event,
    target_fps: float = 20.0,
    max_frames: Optional[int] = None,
):
    interval = 1.0 / target_fps if target_fps > 0 else 0.0
    next_t = time.perf_counter()
    i = 0
    while not stop_evt.is_set() and (max_frames is None or i < max_frames):
        png = make_frame(i, w=1200, h=1000)
        # thread-safe put into asyncio.Queue with backpressure
        fut = asyncio.run_coroutine_threadsafe(q.put((i, png)), loop)
        try:
            fut.result(timeout=5)  # block here if queue is full
        except Exception:
            break

        i += 1
        if interval:
            next_t += interval
            delay = next_t - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            else:
                # we're behind; reset schedule to avoid spiral of death
                next_t = time.perf_counter()


# ---------- async consumer: draws frames ----------
async def consumer_loop(
    q: asyncio.Queue,
    canvas: fc.Canvas,
    stop_evt: threading.Event,
):
    while not stop_evt.is_set():
        try:
            idx, png = await q.get()
        except asyncio.CancelledError:
            break

        print("Draw:", len(png))
        canvas.shapes = [fc.Image(src=png, x=0, y=0)]
        canvas.update()


# ---------- main entry ----------
async def main(page: ft.Page):
    canvas = fc.Canvas(expand=True)
    page.add(canvas)

    loop = asyncio.get_running_loop()
    q: asyncio.Queue = asyncio.Queue(maxsize=100)  # bounded = backpressure
    stop_evt = threading.Event()

    # launch consumer
    consumer = asyncio.create_task(consumer_loop(q, canvas, stop_evt))

    # launch producer in a thread
    t = threading.Thread(
        target=producer_thread,
        args=(loop, q, stop_evt),
        kwargs=dict(target_fps=20.0, max_frames=100),  # tweak as needed
        daemon=True,
    )
    t.start()

    try:
        # wait for producer to finish
        while t.is_alive():
            await asyncio.sleep(0.1)
    finally:
        stop_evt.set()
        t.join(timeout=2)
        if not consumer.done():
            consumer.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await consumer


if __name__ == "__main__":
    ft.run(main)
