import flet as ft
import flet_camera as fc


async def main(page: ft.Page):
    page.title = "Camera control"
    page.padding = 16
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    preview = fc.Camera(
        expand=True,
        preview_enabled=True,
        content=ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.CENTER_FOCUS_STRONG,
                color=ft.Colors.WHITE70,
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
    cameras: list[fc.CameraDescription] = []
    selector = ft.Dropdown(label="Camera", options=[], expand=True)

    async def refresh_cameras(_=None):
        nonlocal cameras
        cameras = await preview.get_available_cameras()
        selector.options = [ft.dropdown.Option(c.name) for c in cameras]
        if cameras and selector.value is None:
            selector.value = cameras[0].name
        selector.update()

    async def init_camera(e=None):
        selected = next(
            (c for c in cameras if c.name == selector.value),
            None,
        )
        if not selected:
            status.value = "No camera selected"
            status.update()
            return
        state = await preview.initialize(
            description=selected,
            resolution_preset=fc.ResolutionPreset.MEDIUM,
            enable_audio=True,
        )
        if state.preview_size:
            status.value = (
                f"Initialized {selected.name} "
                f"({state.preview_size.width}x{state.preview_size.height})"
            )
        else:
            status.value = f"Initialized {selected.name}"
        status.update()

    async def take_photo(_):
        data = await preview.take_picture()
        last_image.src = data
        last_image.update()

    async def on_state_change(e):
        state = e.data if hasattr(e, "data") else e
        if isinstance(state, dict):
            state = fc.CameraState(**state)
        if isinstance(state, fc.CameraState) and state.has_error:
            status.value = f"Camera error: {state.error_description}"
            status.update()

    preview.on_state_change = on_state_change
    selector.on_select = init_camera

    page.add(
        ft.Row(
            [selector, ft.ElevatedButton("Refresh", on_click=refresh_cameras)],
            spacing=12,
        ),
        ft.Container(
            height=320,
            bgcolor=ft.Colors.BLACK,
            border_radius=12,
            padding=8,
            content=preview,
        ),
        ft.Row(
            [
                ft.ElevatedButton("Initialize", on_click=init_camera),
                ft.ElevatedButton("Take photo", on_click=take_photo),
            ],
            spacing=12,
        ),
        status,
        ft.Text("Last photo"),
        last_image,
    )

    await refresh_cameras()
    if selector.value:
        await init_camera()


if __name__ == "__main__":
    ft.run(main)
