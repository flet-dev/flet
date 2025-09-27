from dataclasses import dataclass

import flet as ft
import flet.canvas as cv

MAX_SHAPES_PER_CAPTURE = 30


@dataclass
class State:
    x: float = 0
    y: float = 0
    shapes_count: int = 1


state = State()


def main(page: ft.Page):
    page.title = "Canvas Example"

    file_picker = ft.FilePicker()

    def handle_pan_start(e: ft.DragStartEvent):
        state.x = e.local_position.x
        state.y = e.local_position.y

    async def handle_pan_update(e: ft.DragUpdateEvent):
        ft.context.disable_auto_update()
        canvas.shapes.append(
            cv.Line(
                x1=state.x,
                y1=state.y,
                x2=e.local_position.x,
                y2=e.local_position.y,
                paint=ft.Paint(stroke_width=3),
            )
        )
        canvas.update()
        state.shapes_count += 1

        if state.shapes_count == MAX_SHAPES_PER_CAPTURE:
            await canvas.capture()
            canvas.shapes.clear()
            canvas.update()
            state.shapes_count = 0

        state.x = e.local_position.x
        state.y = e.local_position.y

    canvas = cv.Canvas(
        expand=False,
        shapes=[
            cv.Fill(ft.Paint(color=ft.Colors.WHITE)),
        ],
        content=ft.GestureDetector(
            on_pan_start=handle_pan_start,
            on_pan_update=handle_pan_update,
            drag_interval=10,
        ),
    )

    async def save_image():
        await canvas.capture()
        capture = await canvas.get_capture()
        if capture:
            file_path = await file_picker.save_file(
                file_name="flet_picture.png", src_bytes=capture
            )
            if file_path and page.platform in [
                ft.PagePlatform.MACOS,
                ft.PagePlatform.WINDOWS,
                ft.PagePlatform.LINUX,
            ]:
                with open(file_path, "wb") as f:
                    f.write(capture)

    page.add(
        ft.Button("Save image", on_click=save_image),
        ft.Container(
            content=canvas,
            border_radius=5,
            border=ft.Border.all(2),
            bgcolor=ft.Colors.WHITE,
            width=float("inf"),
            expand=True,
        ),
    )


ft.run(main)
