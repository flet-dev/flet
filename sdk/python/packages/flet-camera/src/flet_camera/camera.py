"""
Camera control definition for the flet-camera package.
"""

from typing import Optional

import flet as ft
from flet.utils import from_dict
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

        Returns:
            A list of available camera descriptions.
        """
        cameras = await self._invoke_method("get_available_cameras")
        return [from_dict(CameraDescription, c) for c in cameras or []]

    async def initialize(
        self,
        description: CameraDescription,
        resolution_preset: ResolutionPreset,
        enable_audio: bool = True,
        fps: Optional[int] = None,
        video_bitrate: Optional[int] = None,
        audio_bitrate: Optional[int] = None,
        image_format_group: Optional[ImageFormatGroup] = None,
    ):
        """
        Initializes a new camera controller for the given description.

        Args:
            description: Camera device to bind to.
            resolution_preset: Desired resolution preset.
            enable_audio: Whether audio is enabled for recordings.
            fps: Optional target frames per second.
            video_bitrate: Optional video bitrate.
            audio_bitrate: Optional audio bitrate.
            image_format_group: Optional image format group override.
        """
        await self._invoke_method(
            "initialize",
            {
                "description": description,
                "resolution_preset": resolution_preset,
                "enable_audio": enable_audio,
                "fps": fps,
                "video_bitrate": video_bitrate,
                "audio_bitrate": audio_bitrate,
                "image_format_group": image_format_group,
            },
        )

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

        Args:
            orientation: Specific orientation to lock, or current
                device orientation if None.
        """
        await self._invoke_method(
            "lock_capture_orientation",
            {"orientation": orientation},
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

        Returns:
            Encoded image bytes.
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

        Returns:
            Encoded video file bytes.
        """
        return await self._invoke_method("stop_video_recording")

    async def supports_image_streaming(self) -> bool:
        """Indicates whether image streaming is supported on the current platform."""
        return await self._invoke_method("supports_image_streaming")

    async def start_image_stream(self):
        """Begins streaming camera image frames."""
        await self._invoke_method("start_image_stream")

    async def stop_image_stream(self):
        """Stops streaming camera image frames."""
        await self._invoke_method("stop_image_stream")

    async def set_description(self, description: CameraDescription):
        """
        Switches to another camera description.

        Args:
            description: Camera to switch to.
        """
        await self._invoke_method("set_description", {"description": description})

    async def set_exposure_mode(self, mode: ExposureMode):
        """Changes the exposure mode.

        Args:
            mode: Exposure mode to apply.
        """
        await self._invoke_method("set_exposure_mode", {"mode": mode})

    async def set_exposure_offset(self, offset: float) -> float:
        """Sets exposure offset in EV units.

        Args:
            offset: Exposure offset to apply.

        Returns:
            The offset value that was set.
        """
        return await self._invoke_method("set_exposure_offset", {"offset": offset})

    async def set_exposure_point(self, point: Optional[ft.OffsetValue]):
        """
        Sets the exposure metering point.

        Args:
            point: Normalized offset (0..1) or None to reset.
        """
        await self._invoke_method("set_exposure_point", {"point": point})

    async def set_flash_mode(self, mode: FlashMode):
        """Changes the flash mode.

        Args:
            mode: Flash mode to apply.
        """
        await self._invoke_method("set_flash_mode", {"mode": mode})

    async def set_focus_mode(self, mode: FocusMode):
        """Changes the focus mode.

        Args:
            mode: Focus mode to apply.
        """
        await self._invoke_method("set_focus_mode", {"mode": mode})

    async def set_focus_point(self, point: Optional[ft.OffsetValue]):
        """
        Sets the focus metering point.

        Args:
            point: Normalized offset (0..1) or None to reset.
        """
        await self._invoke_method("set_focus_point", {"point": point})

    async def set_zoom_level(self, zoom: float):
        """Applies the provided zoom level.

        Args:
            zoom: Zoom level to set.
        """
        await self._invoke_method("set_zoom_level", {"zoom": zoom})

    def before_update(self):
        """Validate platform support prior to sending updates."""
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
