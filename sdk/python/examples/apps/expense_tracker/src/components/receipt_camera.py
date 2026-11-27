"""Rear-camera preview and capture, mounted only in installed mobile apps."""

import logging

import theme

import flet as ft
import flet_camera as fc

log = logging.getLogger(f"app.{__name__}")


@ft.component
def ReceiptCamera(on_capture, on_close):
    camera = ft.use_ref()
    status, set_status = ft.use_state("starting")
    taking, set_taking = ft.use_state(False)
    error, set_error = ft.use_state("")

    async def start():
        try:
            cameras = await camera.current.get_available_cameras()
            if not cameras:
                set_error(
                    "No camera was found. Choose a receipt from your photos instead."
                )
                set_status("error")
                return
            back = next(
                (
                    item
                    for item in cameras
                    if item.lens_direction == fc.CameraLensDirection.BACK
                ),
                cameras[0],
            )
            await camera.current.initialize(
                description=back,
                resolution_preset=fc.ResolutionPreset.HIGH,
                enable_audio=False,
                image_format_group=fc.ImageFormatGroup.JPEG,
            )
            set_status("ready")
        except Exception:
            log.exception("Receipt camera failed to start")
            set_error(
                "The camera couldn't start. Allow camera access in your phone's "
                "Settings, then try again, or choose a photo instead."
            )
            set_status("error")

    ft.use_effect(start, [])

    async def take():
        if taking or status != "ready":
            return
        set_taking(True)
        try:
            data = await camera.current.take_picture()
            on_capture(data)
        except Exception:
            log.exception("Receipt capture failed")
            set_error(
                "Couldn't take the photo. Close the camera and try again, "
                "or choose a photo."
            )
            set_status("error")
        finally:
            set_taking(False)

    return ft.Column(
        tight=True,
        spacing=theme.Space.L,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        "Take receipt photo", expand=True, theme_style=theme.Text.TITLE
                    ),
                    ft.IconButton(
                        ft.Icons.CLOSE,
                        tooltip="Close camera",
                        disabled=taking,
                        on_click=on_close,
                    ),
                ]
            ),
            ft.Text(
                "Starting camera…"
                if status == "starting"
                else "Keep the receipt in frame."
                if status == "ready"
                else error,
                color=ft.Colors.ON_SURFACE_VARIANT,
            ),
            ft.Container(
                height=theme.CAMERA_PREVIEW_HEIGHT,
                border_radius=theme.Radius.M,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.Alignment.CENTER,
                content=fc.Camera(ref=camera, expand=True, preview_enabled=True)
                if status != "error"
                else ft.Icon(ft.Icons.PHOTO_CAMERA, color=ft.Colors.WHITE),
            ),
            ft.FilledButton(
                "Taking photo…" if taking else "Use photo",
                icon=ft.Icons.PHOTO_CAMERA,
                disabled=status != "ready" or taking,
                on_click=take,
            ),
        ],
    )
