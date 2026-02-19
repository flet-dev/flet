import logging
from dataclasses import dataclass, field
from datetime import datetime

import flet as ft
import flet_camera as fc

logging.basicConfig(level=logging.INFO)


@dataclass
class State:
    cameras: list[fc.CameraDescription] = field(default_factory=list)
    selected_camera: fc.CameraDescription | None = None
    camera_labels: dict[str, str] = field(default_factory=dict)


async def main(page: ft.Page):
    page.title = "Camera control"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO
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
    selector = ft.Dropdown(label="Select camera", options=[])
    recorded_video_path = ft.Text(value="Recorded video: not saved yet", size=12)

    def has_human_readable_name(camera: fc.CameraDescription) -> bool:
        name = camera.name.strip()
        if not name:
            return False
        if name.startswith("com.apple.avfoundation."):
            return False
        return not (":" in name and "." in name)

    def camera_label(camera: fc.CameraDescription) -> str:
        if has_human_readable_name(camera):
            return camera.name

        direction = camera.lens_direction.value.capitalize()
        lens_map = {
            "wide": "Wide",
            "telephoto": "Telephoto",
            "ultraWide": "Ultra Wide",
            "unknown": "Unknown",
        }
        lens_type = lens_map.get(camera.lens_type.value, camera.lens_type.value)
        return f"{direction} ({lens_type})"

    def detect_video_extension(data: bytes) -> str:
        # Matroska/WebM EBML header.
        if data.startswith(b"\x1a\x45\xdf\xa3"):
            return "webm"

        # ISO BMFF (mp4/mov) starts with a box size + "ftyp".
        if len(data) >= 12 and data[4:8] == b"ftyp":
            brand = data[8:12]
            if brand == b"qt  ":
                return "mov"
            return "mp4"

        return "bin"

    async def get_cameras():
        state.cameras = await preview.get_available_cameras()
        state.camera_labels.clear()
        seen_labels: dict[str, int] = {}
        for camera in state.cameras:
            label = camera_label(camera)
            seen_labels[label] = seen_labels.get(label, 0) + 1
            if seen_labels[label] > 1:
                label = f"{label} {seen_labels[label]}"
            state.camera_labels[camera.name] = label

        selector.options = [
            ft.DropdownOption(key=c.name, text=state.camera_labels[c.name])
            for c in state.cameras
        ]
        if selector.value and selector.value not in state.camera_labels:
            selector.value = None
        status.value = "Select a camera"
        page.update()

    async def init_camera(e=None):
        state.selected_camera = next(
            (c for c in state.cameras if c.name == selector.value),
            None,
        )
        if not state.selected_camera:
            status.value = "No camera selected"
            return

        selected_label = state.camera_labels.get(
            state.selected_camera.name, state.selected_camera.name
        )
        status.value = f"Initializing {selected_label}"
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

    async def start_recording(_):
        await preview.prepare_for_video_recording()
        await preview.start_video_recording()
        status.value = "Recording video..."
        status.update()

    async def pause_recording(_):
        await preview.pause_video_recording()
        status.value = "Recording paused"
        status.update()

    async def resume_recording(_):
        await preview.resume_video_recording()
        status.value = "Recording resumed"
        status.update()

    async def stop_recording(_):
        data = await preview.stop_video_recording()
        if not data:
            status.value = "No video data returned"
            status.update()
            return

        ext = detect_video_extension(data)
        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        saved_path = await ft.FilePicker().save_file(
            file_name=filename,
            src_bytes=data,
        )

        kb_size = len(data) / 1024
        status.value = f"Video recorded: {kb_size:.1f} KB"
        if saved_path:
            recorded_video_path.value = f"Recorded video: {saved_path}"
        else:
            recorded_video_path.value = "Recorded video save canceled"
        page.update()

    async def on_state_change(e: ft.Event[fc.CameraState]):
        if e.description == state.selected_camera:
            print("Camera state changed:", e)
            if e.has_error:
                status.value = f"Camera error: {e.error_description}"
            elif e.is_taking_picture:
                status.value = "Taking picture..."
            elif e.is_recording_paused:
                status.value = "Recording paused"
            elif e.is_recording_video:
                status.value = "Recording video..."
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
        try:
            last_image.src = e.bytes
            last_image.update()
        except Exception as ex:
            logging.exception("Failed to render stream frame: %s", ex)

    preview.on_stream_image = on_stream_image

    async def pause_preview():
        await preview.pause_preview()

    async def resume_preview():
        await preview.resume_preview()

    page.on_connect = get_cameras

    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            selector,
                            ft.IconButton(ft.Icons.REFRESH, on_click=get_cameras),
                        ],
                        wrap=True,
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
                            ft.Button("Start rec", on_click=start_recording),
                            ft.Button("Pause rec", on_click=pause_recording),
                            ft.Button("Resume rec", on_click=resume_recording),
                            ft.Button("Stop rec", on_click=stop_recording),
                        ],
                        wrap=True,
                    ),
                    ft.Row(
                        [
                            ft.Button("Start streaming", on_click=start_streaming),
                            ft.Button("Stop streaming", on_click=stop_streaming),
                        ],
                        wrap=True,
                    ),
                    ft.Row(
                        [
                            ft.Button("Pause preview", on_click=pause_preview),
                            ft.Button("Resume preview", on_click=resume_preview),
                        ],
                        wrap=True,
                    ),
                    recorded_video_path,
                    ft.Text("Last photo"),
                    last_image,
                ]
            )
        )
    )

    await get_cameras()


if __name__ == "__main__":
    ft.run(main)
