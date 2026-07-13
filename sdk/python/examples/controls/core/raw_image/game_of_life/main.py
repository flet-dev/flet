import asyncio
import time
from collections import deque

import numpy as np

import flet as ft

GRID_WIDTH = 160
GRID_HEIGHT = 100
CELL_SIZE = 5  # logical pixels per cell on screen
FPS_WINDOW_SECONDS = 2.0

ALIVE_COLOR = (80, 250, 123)
DEAD_COLOR = (30, 32, 44)


def step(world: np.ndarray) -> np.ndarray:
    """One Game of Life generation on a wrapping (toroidal) grid."""
    neighbors = sum(
        np.roll(np.roll(world, dy, axis=0), dx, axis=1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if (dy, dx) != (0, 0)
    )
    return (neighbors == 3) | (world & (neighbors == 2))


def world_frame(world: np.ndarray) -> np.ndarray:
    frame = np.empty((GRID_HEIGHT, GRID_WIDTH, 4), dtype=np.uint8)
    frame[..., :3] = np.where(world[..., None], ALIVE_COLOR, DEAD_COLOR)
    frame[..., 3] = 255
    return frame


async def main(page: ft.Page):
    page.title = "RawImage Game of Life"

    rng = np.random.default_rng(42)
    world = rng.random((GRID_HEIGHT, GRID_WIDTH)) < 0.2

    # One frame pixel per cell: the client upscales with nearest-neighbor
    # (filter_quality=NONE), so each cell stays a crisp square and frames
    # remain tiny (grid-sized) regardless of the on-screen size.
    raw_image = ft.RawImage(
        width=GRID_WIDTH * CELL_SIZE,
        height=GRID_HEIGHT * CELL_SIZE,
        fit=ft.BoxFit.FILL,
        filter_quality=ft.FilterQuality.NONE,
    )

    playing = True
    dirty = asyncio.Event()
    frame_times: deque[float] = deque()

    def toggle_playing():
        nonlocal playing
        playing = not playing
        play_button.icon = ft.Icons.PAUSE if playing else ft.Icons.PLAY_ARROW
        play_button.update()
        dirty.set()

    def randomize():
        nonlocal world
        world = rng.random((GRID_HEIGHT, GRID_WIDTH)) < 0.2
        dirty.set()

    def clear():
        nonlocal world
        world = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=bool)
        dirty.set()

    def paint_cell(position: ft.Offset):
        # Draw with the pointer, also while the simulation is running.
        x = int(position.x // CELL_SIZE)
        y = int(position.y // CELL_SIZE)
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            world[y, x] = True
            dirty.set()

    play_button = ft.IconButton(ft.Icons.PAUSE, on_click=toggle_playing)
    speed_slider = ft.Slider(min=1, max=60, value=20, width=150)
    fps_text = ft.Text("fps: —", size=12)

    page.add(
        ft.Row(
            [
                play_button,
                ft.Text("speed:"),
                speed_slider,
                ft.OutlinedButton("Randomize", on_click=randomize),
                ft.OutlinedButton("Clear", on_click=clear),
                fps_text,
            ],
            spacing=10,
        ),
        ft.GestureDetector(
            content=raw_image,
            on_tap_down=lambda e: paint_cell(e.local_position),
            on_pan_update=lambda e: paint_cell(e.local_position),
            drag_interval=10,
        ),
    )

    async def run_loop():
        nonlocal world
        while True:
            if playing:
                world = step(world)
                dirty.clear()
            else:
                # Paused: wait for pointer edits or the play button.
                await dirty.wait()
                dirty.clear()
            try:
                await raw_image.render(world_frame(world), premultiplied=True)
            except (RuntimeError, TimeoutError):
                return  # window closed — session destroyed
            now = time.monotonic()
            frame_times.append(now)
            while frame_times and frame_times[0] < now - FPS_WINDOW_SECONDS:
                frame_times.popleft()
            fps_text.value = f"fps: {len(frame_times) / FPS_WINDOW_SECONDS:.1f}"
            try:
                page.update()
            except RuntimeError:
                return
            if playing:
                await asyncio.sleep(1 / speed_slider.value)

    asyncio.create_task(run_loop())


if __name__ == "__main__":
    ft.run(main)
