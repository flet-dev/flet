"""
Camera control definition for the flet-camera package.
"""

from typing import Optional

import flet as ft
from flet_camera.types import (
    CameraDescription,
    CameraImage,
    CameraState,
    DeviceOrientation,
    ExposureMode,
    FlashMode,
    FocusMode,
    ImageFormatGroup,
    ResolutionPreset,
)

__all__ = ["Camera"]


def _enum_to_value(value):
    return value.value if hasattr(value, "value") else value


@ft.control("Camera")
class Camera(ft.LayoutControl):
    """
    A control that provides camera preview and capture capabilities.
    """

    preview_enabled: bool = True
    """
    Whether the preview surface is shown.
    """

    content: Optional[ft.Control] = None
    """
    Optional child to overlay on top of the camera preview.
    """

    on_state_change: Optional[ft.EventHandler[CameraState]] = None
    """Fires when the camera controller state changes."""

    on_stream_image: Optional[ft.EventHandler[CameraImage]] = None
    """
    Fires when an image frame is available while streaming.
    """

    async def get_available_cameras(self) -> list[CameraDescription]:
        """
        Lists the available camera devices on the current platform.
        """
        cameras = await self._invoke_method("get_available_cameras")
        return [CameraDescription(**c) for c in cameras or []]

    async def initialize(
        self,
        description: CameraDescription,
        resolution_preset: ResolutionPreset,
        enable_audio: bool = True,
        fps: Optional[int] = None,
        video_bitrate: Optional[int] = None,
        audio_bitrate: Optional[int] = None,
        image_format_group: Optional[ImageFormatGroup] = None,
    ) -> CameraState:
        """
        Initializes a new camera controller for the given description.
        """
        state = await self._invoke_method(
            "initialize",
            {
                "description": description,
                "resolution_preset": _enum_to_value(resolution_preset),
                "enable_audio": enable_audio,
                "fps": fps,
                "video_bitrate": video_bitrate,
                "audio_bitrate": audio_bitrate,
                "image_format_group": _enum_to_value(image_format_group),
            },
        )
        return CameraState(**state)

    async def get_exposure_offset_step_size(self) -> float:
        """Returns the smallest increment supported for exposure offset changes."""
        return await self._invoke_method("get_exposure_offset_step_size")

    async def get_max_exposure_offset(self) -> float:
        """Maximum exposure offset supported by the current camera."""
        return await self._invoke_method("get_max_exposure_offset")

    async def get_max_zoom_level(self) -> float:
        """Maximum zoom level supported by the current camera."""
        return await self._invoke_method("get_max_zoom_level")

    async def get_min_exposure_offset(self) -> float:
        """Minimum exposure offset supported by the current camera."""
        return await self._invoke_method("get_min_exposure_offset")

    async def get_min_zoom_level(self) -> float:
        """Minimum zoom level supported by the current camera."""
        return await self._invoke_method("get_min_zoom_level")

    async def lock_capture_orientation(
        self, orientation: Optional[DeviceOrientation] = None
    ):
        """
        Locks capture orientation to the specified device orientation.
        """
        await self._invoke_method(
            "lock_capture_orientation",
            {"orientation": _enum_to_value(orientation)},
        )

    async def unlock_capture_orientation(self):
        """Unlocks the capture orientation."""
        await self._invoke_method("unlock_capture_orientation")

    async def pause_preview(self):
        """Pauses the camera preview."""
        await self._invoke_method("pause_preview")

    async def resume_preview(self):
        """Resumes the camera preview."""
        await self._invoke_method("resume_preview")

    async def take_picture(self) -> bytes:
        """
        Captures a still image and returns the encoded bytes.
        """
        return await self._invoke_method("take_picture")

    async def prepare_for_video_recording(self):
        """Prepares the capture session for video recording."""
        await self._invoke_method("prepare_for_video_recording")

    async def start_video_recording(self):
        """Starts capturing video."""
        await self._invoke_method("start_video_recording")

    async def pause_video_recording(self):
        """Pauses an active video recording."""
        await self._invoke_method("pause_video_recording")

    async def resume_video_recording(self):
        """Resumes a paused video recording."""
        await self._invoke_method("resume_video_recording")

    async def stop_video_recording(self) -> bytes:
        """
        Stops video recording and returns the recorded bytes.
        """
        return await self._invoke_method("stop_video_recording")

    async def start_image_stream(self):
        """Begins streaming camera image frames."""
        await self._invoke_method("start_image_stream")

    async def stop_image_stream(self):
        """Stops streaming camera image frames."""
        await self._invoke_method("stop_image_stream")

    async def set_description(self, description: CameraDescription):
        """
        Switches to another camera description.
        """
        await self._invoke_method("set_description", {"description": description})

    async def set_exposure_mode(self, mode: ExposureMode):
        """Changes the exposure mode."""
        await self._invoke_method("set_exposure_mode", {"mode": _enum_to_value(mode)})

    async def set_exposure_offset(self, offset: float) -> float:
        """Sets exposure offset in EV units."""
        return await self._invoke_method("set_exposure_offset", {"offset": offset})

    async def set_exposure_point(self, point: Optional[ft.OffsetValue]):
        """
        Sets the exposure metering point.
        """
        await self._invoke_method("set_exposure_point", {"point": point})

    async def set_flash_mode(self, mode: FlashMode):
        """Changes the flash mode."""
        await self._invoke_method("set_flash_mode", {"mode": _enum_to_value(mode)})

    async def set_focus_mode(self, mode: FocusMode):
        """Changes the focus mode."""
        await self._invoke_method("set_focus_mode", {"mode": _enum_to_value(mode)})

    async def set_focus_point(self, point: Optional[ft.OffsetValue]):
        """
        Sets the focus metering point.
        """
        await self._invoke_method("set_focus_point", {"point": point})

    async def set_zoom_level(self, zoom: float):
        """Applies the provided zoom level."""
        await self._invoke_method("set_zoom_level", {"zoom": zoom})

    def before_update(self):
        super().before_update()

        # validate platform
        if not (
            self.page.web
            or self.page.platform
            in [
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.IOS,
            ]
        ):
            raise ft.FletUnsupportedPlatformException(
                "Camera is currently only supported on Android, iOS and Web platforms."
            )
