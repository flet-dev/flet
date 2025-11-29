import logging
from dataclasses import dataclass, field

import flet as ft
import flet_camera as fc

logging.basicConfig(level=logging.INFO)


@dataclass
class State:
    cameras: list[fc.CameraDescription] = field(default_factory=list)
    selected_camera: fc.CameraDescription | None = None


async def main(page: ft.Page):
    page.title = "Camera control"
    page.padding = 16
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    state = State()

    preview = fc.Camera(
        expand=True,
        preview_enabled=True,
        content=ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.CENTER_FOCUS_STRONG,
                color=ft.Colors.WHITE_70,
                size=48,
            ),
        ),
    )

    status = ft.Text(value="Select a camera", size=12)
    last_image = ft.Image(
        src="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wIAAgMBAp0YVwAAAABJRU5ErkJggg==",
        height=200,
        fit=ft.BoxFit.CONTAIN,
    )
    selector = ft.Dropdown(label="Camera", options=[])

    async def get_cameras():
        state.cameras = await preview.get_available_cameras()
        selector.options = [ft.DropdownOption(c.name) for c in state.cameras]
        if state.cameras and selector.value is None:
            selector.value = state.cameras[0].name
        if selector.value:
            await init_camera()

    async def init_camera(e=None):
        state.selected_camera = next(
            (c for c in state.cameras if c.name == selector.value),
            None,
        )
        if not state.selected_camera:
            status.value = "No camera selected"
            return

        status.value = f"Initializing {state.selected_camera.name}"
        status.update()
        await preview.initialize(
            description=state.selected_camera,
            resolution_preset=fc.ResolutionPreset.MEDIUM,
            enable_audio=True,
        )

    async def take_photo(_):
        data = await preview.take_picture()
        last_image.src = data
        last_image.update()

    async def on_state_change(e: ft.Event[fc.CameraState]):
        if e.description == state.selected_camera:
            print("Camera state changed:", e)
            if e.has_error:
                status.value = f"Camera error: {e.error_description}"
            elif e.is_taking_picture:
                status.value = "Taking picture..."
            elif e.is_recording_video:
                status.value = "Recording video..."
            elif e.is_recording_paused:
                status.value = "Recording paused"
            elif e.is_streaming_images:
                status.value = "Streaming images..."
            elif e.is_preview_paused:
                status.value = "Preview paused"
            else:
                status.value = "Camera ready"

    preview.on_state_change = on_state_change
    selector.on_select = init_camera

    async def start_streaming():
        await preview.start_image_stream()

    async def stop_streaming():
        await preview.stop_image_stream()

    def on_stream_image(e: ft.Event[fc.CameraImage]):
        print("Stream image received:", e)

    preview.on_stream_image = on_stream_image

    async def pause_preview():
        await preview.pause_preview()

    async def resume_preview():
        await preview.resume_preview()

    page.on_connect = get_cameras

    page.add(
        ft.Row(
            [
                selector,
                ft.IconButton(ft.Icons.REFRESH, on_click=get_cameras),
            ],
        ),
        ft.Container(
            height=320,
            bgcolor=ft.Colors.BLACK,
            border_radius=3,
            content=preview,
        ),
        status,
        ft.Row(
            [
                ft.Button("Take photo", on_click=take_photo),
                ft.Button("Start streaming", on_click=start_streaming),
                ft.Button("Stop streaming", on_click=stop_streaming),
            ],
        ),
        ft.Row(
            [
                ft.Button("Pause preview", on_click=pause_preview),
                ft.Button("Resume preview", on_click=resume_preview),
            ]
        ),
        ft.Text("Last photo"),
        last_image,
    )

    await get_cameras()


if __name__ == "__main__":
    ft.run(main)
