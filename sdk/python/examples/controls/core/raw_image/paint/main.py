import asyncio

from PIL import Image, ImageDraw

import flet as ft

CANVAS_WIDTH = 700
CANVAS_HEIGHT = 450
# ImageDraw has no anti-aliasing: lines and ellipses get hard, jagged
# edges. Painting on a canvas this many times larger and letting the
# client downscale it into the control's box averages each screen pixel
# from SUPERSAMPLE^2 canvas pixels — cheap, GPU-side anti-aliasing.
SUPERSAMPLE = 2
PALETTE = [
    "#1d1d21",
    "#e53935",
    "#fb8c00",
    "#fdd835",
    "#43a047",
    "#1e88e5",
    "#8e24aa",
]


async def main(page: ft.Page):
    page.title = "RawImage paint"

    image = Image.new(
        "RGBA", (CANVAS_WIDTH * SUPERSAMPLE, CANVAS_HEIGHT * SUPERSAMPLE), "white"
    )
    draw = ImageDraw.Draw(image)

    # Frames arrive at SUPERSAMPLE times the control's size; fit=FILL
    # scales them down and filter_quality blends the extra pixels away.
    raw_image = ft.RawImage(
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        fit=ft.BoxFit.FILL,
        filter_quality=ft.FilterQuality.MEDIUM,
    )

    brush_color = PALETTE[0]
    last_point: tuple[float, float] | None = None  # in canvas pixels

    # Pan events arrive faster than frames can be displayed, so handlers
    # only mutate the Pillow image and flag it dirty; a single loop below
    # streams the latest state as fast as the display confirms frames.
    dirty = asyncio.Event()

    def stroke_to(point: ft.Offset):
        nonlocal last_point
        # Pointer coordinates are in control (logical) pixels; the canvas
        # lives at SUPERSAMPLE resolution.
        x = point.x * SUPERSAMPLE
        y = point.y * SUPERSAMPLE
        radius = brush_size_slider.value / 2 * SUPERSAMPLE
        if last_point is not None:
            draw.line(
                (last_point[0], last_point[1], x, y),
                fill=brush_color,
                width=int(radius * 2),
            )
        # Round cap: a line alone leaves flat, jagged joints.
        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=brush_color,
        )
        last_point = (x, y)
        dirty.set()

    def pan_start(e: ft.DragStartEvent):
        nonlocal last_point
        last_point = None
        stroke_to(e.local_position)

    def pan_update(e: ft.DragUpdateEvent):
        stroke_to(e.local_position)

    def select_color(color: str):
        nonlocal brush_color
        brush_color = color
        for dot in palette_row.controls:
            dot.border = (
                ft.Border.all(3, ft.Colors.BLUE_GREY_200) if dot.data == color else None
            )
        palette_row.update()

    def clear_canvas():
        draw.rectangle(
            (0, 0, CANVAS_WIDTH * SUPERSAMPLE, CANVAS_HEIGHT * SUPERSAMPLE),
            fill="white",
        )
        dirty.set()

    palette_row = ft.Row(
        [
            ft.Container(
                width=28,
                height=28,
                border_radius=14,
                bgcolor=color,
                data=color,
                on_click=lambda e: select_color(e.control.data),
            )
            for color in PALETTE
        ],
        spacing=8,
    )
    brush_size_slider = ft.Slider(min=2, max=40, value=8, width=150)

    page.add(
        ft.Row(
            [
                palette_row,
                ft.Text("size:"),
                brush_size_slider,
                ft.OutlinedButton("Clear", on_click=clear_canvas),
            ],
            spacing=10,
        ),
        ft.Container(
            content=ft.GestureDetector(
                content=raw_image,
                on_pan_start=pan_start,
                on_pan_update=pan_update,
                drag_interval=10,
            ),
            border=ft.Border.all(1, ft.Colors.BLUE_GREY_200),
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
        ),
    )
    select_color(brush_color)

    async def render_loop():
        while True:
            await dirty.wait()
            dirty.clear()
            try:
                # The canvas is opaque, so it is premultiplied by definition.
                # Awaiting the render paces this loop to display speed: any
                # strokes drawn meanwhile coalesce into the next frame.
                await raw_image.render(image, premultiplied=True)
            except (RuntimeError, TimeoutError):
                return  # window closed — session destroyed

    dirty.set()  # show the blank canvas
    asyncio.create_task(render_loop())


if __name__ == "__main__":
    ft.run(main)
