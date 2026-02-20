import base64
import logging
from dataclasses import dataclass, field
from datetime import datetime
from math import cos, pi, sin

import flet as ft
import flet_camera as fc


@dataclass
class State:
    cameras: list[fc.CameraDescription] = field(default_factory=list)
    selected_camera: fc.CameraDescription | None = None
    camera_labels: dict[str, str] = field(default_factory=dict)
    is_streaming: bool = False
    is_streaming_supported: bool = False
    is_initialized: bool = False
    is_preview_paused: bool = False
    is_recording: bool = False
    is_recording_paused: bool = False
    device_orientation: fc.DeviceOrientation | None = None
    last_frame_width: int | None = None
    last_frame_height: int | None = None


async def main(page: ft.Page):
    image_frame_width = 280
    image_frame_height = 200
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
    last_photo_label = ft.Text("Last photo", visible=False)
    last_image = ft.Image(
        src=base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wIAAgMBAp0YVwAAAABJRU5ErkJggg=="
        ),
        width=image_frame_width,
        height=image_frame_height,
        fit=ft.BoxFit.CONTAIN,
        gapless_playback=True,
    )
    last_image_frame = ft.Container(
        width=image_frame_width,
        height=image_frame_height,
        alignment=ft.Alignment.CENTER,
        content=last_image,
        visible=False,
    )
    selector = ft.Dropdown(label="Camera", options=[])
    recorded_video_path = ft.Text(value="Recorded video: not saved yet", size=12)
    take_photo_btn = ft.FilledIconButton(
        icon=ft.Icons.PHOTO_CAMERA,
        tooltip="Take photo",
        disabled=True,
    )
    record_btn = ft.FilledTonalIconButton(
        icon=ft.Icons.VIDEOCAM,
        selected_icon=ft.Icons.STOP,
        selected=False,
        tooltip="Start / stop recording",
        disabled=True,
    )
    pause_recording_btn = ft.OutlinedIconButton(
        icon=ft.Icons.PAUSE,
        selected_icon=ft.Icons.PLAY_ARROW,
        selected=False,
        tooltip="Pause / resume recording",
        disabled=True,
    )
    stream_btn = ft.OutlinedIconButton(
        icon=ft.Icons.PLAY_ARROW,
        selected_icon=ft.Icons.STOP,
        selected=False,
        tooltip="Start / stop image stream",
        disabled=True,
    )
    preview_btn = ft.OutlinedIconButton(
        icon=ft.Icons.VISIBILITY_OFF,
        selected_icon=ft.Icons.VISIBILITY,
        selected=True,
        tooltip="Pause / resume preview",
        disabled=True,
    )

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

    def device_orientation_degrees(orientation: fc.DeviceOrientation | None) -> int:
        if orientation == ft.DeviceOrientation.PORTRAIT_UP:
            return 0
        if orientation == ft.DeviceOrientation.LANDSCAPE_RIGHT:
            return 90
        if orientation == ft.DeviceOrientation.PORTRAIT_DOWN:
            return 180
        if orientation == ft.DeviceOrientation.LANDSCAPE_LEFT:
            return 270
        return 0

    def image_rotation_radians() -> float:
        camera = state.selected_camera
        if camera is None:
            return 0.0
        sensor_orientation = camera.sensor_orientation
        device_degrees = device_orientation_degrees(state.device_orientation)
        if camera.lens_direction == fc.CameraLensDirection.FRONT:
            rotation_degrees = (sensor_orientation + device_degrees) % 360
        else:
            rotation_degrees = (sensor_orientation - device_degrees + 360) % 360
        return rotation_degrees * pi / 180

    def apply_last_image_transform(src_width: int | None, src_height: int | None):
        _ = (src_width, src_height)
        last_image.width = image_frame_width
        last_image.height = image_frame_height
        angle = image_rotation_radians()
        width = float(image_frame_width)
        height = float(image_frame_height)
        calc_angle = -angle

        # Flet uses clockwise radians for Rotate.angle.
        def rotate_point(x: float, y: float) -> tuple[float, float]:
            return (
                x * cos(calc_angle) + y * sin(calc_angle),
                -x * sin(calc_angle) + y * cos(calc_angle),
            )

        corners = [
            rotate_point(0.0, 0.0),
            rotate_point(width, 0.0),
            rotate_point(0.0, height),
            rotate_point(width, height),
        ]
        min_x = min(p[0] for p in corners)
        min_y = min(p[1] for p in corners)

        # Control.offset is normalized by control width/height.
        last_image.offset = ft.Offset(
            x=(-min_x / width) if width else 0.0,
            y=(-min_y / height) if height else 0.0,
        )
        last_image.rotate = ft.Rotate(angle=angle, alignment=ft.Alignment.TOP_LEFT)

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
        state.selected_camera = None
        state.is_initialized = False
        state.is_streaming = False
        state.is_recording = False
        state.is_recording_paused = False
        state.is_preview_paused = False
        state.is_streaming_supported = False
        state.device_orientation = None
        sync_action_buttons()
        status.value = "Select a camera"
        page.update()

    def sync_action_buttons():
        take_photo_btn.disabled = not state.is_initialized
        record_btn.disabled = not state.is_initialized
        record_btn.selected = state.is_recording
        pause_recording_btn.selected = state.is_recording_paused
        pause_recording_btn.disabled = not state.is_recording
        stream_btn.selected = state.is_streaming
        stream_btn.disabled = not (
            state.is_initialized and state.is_streaming_supported
        )
        preview_btn.selected = not state.is_preview_paused
        preview_btn.disabled = not state.is_initialized

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
            image_format_group=fc.ImageFormatGroup.JPEG,
        )
        if not page.web:
            try:
                await preview.lock_capture_orientation()
            except RuntimeError as ex:
                logging.warning("Could not lock capture orientation: %s", ex)
        state.is_initialized = True
        state.is_streaming = False
        state.is_streaming_supported = await preview.supports_image_streaming()
        sync_action_buttons()
        page.update()

    async def take_photo():
        if not state.is_initialized:
            status.value = "Initialize camera first"
            page.update()
            return
        data = await preview.take_picture()
        last_image.src = data
        apply_last_image_transform(state.last_frame_width, state.last_frame_height)
        last_photo_label.visible = True
        last_image_frame.visible = True
        page.update()

    async def start_recording():
        if not state.is_initialized:
            status.value = "Initialize camera first"
            page.update()
            return
        await preview.prepare_for_video_recording()
        await preview.start_video_recording()
        state.is_recording = True
        state.is_recording_paused = False
        sync_action_buttons()
        status.value = "Recording video..."
        page.update()

    async def pause_recording():
        if not state.is_initialized or not state.is_recording:
            return
        await preview.pause_video_recording()
        state.is_recording_paused = True
        sync_action_buttons()
        status.value = "Recording paused"
        page.update()

    async def resume_recording():
        if not state.is_initialized or not state.is_recording:
            return
        await preview.resume_video_recording()
        state.is_recording_paused = False
        sync_action_buttons()
        status.value = "Recording resumed"
        page.update()

    async def stop_recording():
        if not state.is_initialized or not state.is_recording:
            return
        data = await preview.stop_video_recording()
        state.is_recording = False
        state.is_recording_paused = False
        sync_action_buttons()
        if not data:
            status.value = "No video data returned"
            page.update()
            return

        ext = fc.detect_video_extension(data)
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

    async def on_state_change(e: fc.CameraStateEvent):
        if e.description == state.selected_camera:
            state.device_orientation = e.device_orientation
            state.is_recording = e.is_recording_video
            state.is_recording_paused = e.is_recording_paused
            state.is_streaming = e.is_streaming_images
            state.is_preview_paused = e.is_preview_paused
            sync_action_buttons()
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
            page.update()

    preview.on_state_change = on_state_change
    selector.on_select = init_camera

    async def start_streaming():
        if not state.is_initialized:
            status.value = "Initialize camera first"
            page.update()
            return
        if not state.is_streaming_supported:
            status.value = "Image streaming is not supported by this camera"
            page.update()
            return
        await preview.start_image_stream()
        state.is_streaming = True
        sync_action_buttons()
        page.update()

    async def stop_streaming():
        if not state.is_initialized:
            return
        await preview.stop_image_stream()
        state.is_streaming = False
        sync_action_buttons()
        page.update()

    def on_stream_image(e: fc.CameraImageEvent):
        try:
            state.last_frame_width = e.width
            state.last_frame_height = e.height
            last_image.src = e.bytes
            apply_last_image_transform(e.width, e.height)
            last_photo_label.visible = True
            last_image_frame.visible = True
            page.update()
        except Exception as ex:
            logging.exception("Failed to render stream frame: %s", ex)

    preview.on_stream_image = on_stream_image

    async def pause_preview():
        if not state.is_initialized:
            return
        await preview.pause_preview()
        state.is_preview_paused = True
        sync_action_buttons()
        page.update()

    async def resume_preview():
        if not state.is_initialized:
            return
        await preview.resume_preview()
        state.is_preview_paused = False
        sync_action_buttons()
        page.update()

    async def toggle_recording():
        if state.is_recording:
            await stop_recording()
        else:
            await start_recording()

    async def toggle_recording_pause():
        if state.is_recording_paused:
            await resume_recording()
        else:
            await pause_recording()

    async def toggle_streaming():
        if state.is_streaming:
            await stop_streaming()
        else:
            await start_streaming()

    async def toggle_preview():
        if state.is_preview_paused:
            await resume_preview()
        else:
            await pause_preview()

    take_photo_btn.on_click = take_photo
    record_btn.on_click = toggle_recording
    pause_recording_btn.on_click = toggle_recording_pause
    stream_btn.on_click = toggle_streaming
    preview_btn.on_click = toggle_preview

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
                            take_photo_btn,
                            record_btn,
                            pause_recording_btn,
                            stream_btn,
                            preview_btn,
                        ],
                        wrap=True,
                    ),
                    recorded_video_path,
                    last_photo_label,
                    last_image_frame,
                ]
            )
        )
    )

    await get_cameras()


if __name__ == "__main__":
    ft.run(main)
