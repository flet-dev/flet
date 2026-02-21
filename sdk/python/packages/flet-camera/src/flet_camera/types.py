from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    from flet_camera.camera import Camera  # noqa

__all__ = [
    "CameraDescription",
    "CameraImageEvent",
    "CameraLensDirection",
    "CameraLensType",
    "CameraPreviewSize",
    "CameraStateEvent",
    "ExposureMode",
    "FlashMode",
    "FocusMode",
    "ImageFormatGroup",
    "ResolutionPreset",
]


class ResolutionPreset(Enum):
    """Represents a capture resolution preset."""

    LOW = "low"
    """Low resolution preset."""
    MEDIUM = "medium"
    """Medium resolution preset."""
    HIGH = "high"
    """High resolution preset."""
    VERY_HIGH = "veryHigh"
    """Very high resolution preset."""
    ULTRA_HIGH = "ultraHigh"
    """Ultra high resolution preset."""
    MAX = "max"
    """Maximum available resolution preset."""


class ImageFormatGroup(Enum):
    """Describes the image output format."""

    BGRA8888 = "bgra8888"
    """Raw BGRA 8888 format."""
    JPEG = "jpeg"
    """JPEG-compressed format."""
    NV21 = "nv21"
    """NV21 YUV format (Android)."""
    YUV420 = "yuv420"
    """YUV420 planar format."""
    UNKNOWN = "unknown"
    """Unknown or unsupported format."""


class FlashMode(Enum):
    """Flash modes supported by the camera."""

    OFF = "off"
    """Disable flash."""
    AUTO = "auto"
    """Use flash automatically when required."""
    ALWAYS = "always"
    """Always fire flash."""
    TORCH = "torch"
    """Continuous torch/flashlight mode."""


class ExposureMode(Enum):
    """Exposure modes supported by the camera."""

    AUTO = "auto"
    """Automatic exposure."""
    LOCKED = "locked"
    """Lock exposure to the current value."""


class FocusMode(Enum):
    """Focus modes supported by the camera."""

    AUTO = "auto"
    """Automatic focus."""
    LOCKED = "locked"
    """Lock focus to the current value."""


class CameraLensDirection(Enum):
    """Direction the camera is facing."""

    FRONT = "front"
    """Front facing camera."""
    BACK = "back"
    """Back facing camera."""
    EXTERNAL = "external"
    """External camera device."""


class CameraLensType(Enum):
    """Type of the camera lens."""

    WIDE = "wide"
    """Wide-angle lens."""
    TELEPHOTO = "telephoto"
    """Telephoto lens."""
    ULTRA_WIDE = "ultraWide"
    """Ultra-wide lens."""
    UNKNOWN = "unknown"
    """Unknown lens type."""


@dataclass
class CameraPreviewSize:
    """Dimensions of a camera preview."""

    width: ft.Number
    """Preview width in logical pixels."""

    height: ft.Number
    """Preview height in logical pixels."""


@dataclass
class CameraDescription:
    """Properties of a camera device."""

    name: str
    """Human-readable identifier of the camera device."""

    lens_direction: CameraLensDirection
    """Physical lens direction (front, back, external)."""

    sensor_orientation: int
    """Clockwise angle (0, 90, 180, 270) needed to display upright output."""

    lens_type: CameraLensType = CameraLensType.UNKNOWN
    """Lens hardware type (wide, telephoto, ultra-wide, or unknown)."""


@dataclass
class CameraStateEvent(ft.Event["Camera"]):
    """Snapshot of the camera controller state."""

    is_initialized: bool
    """Whether the controller has been initialized."""

    is_recording_video: bool
    """Whether a video recording is in progress."""

    is_recording_paused: bool
    """Whether an active recording is currently paused."""

    is_taking_picture: bool
    """True while a still capture is underway."""

    is_streaming_images: bool
    """True when image streaming is running."""

    is_preview_paused: bool
    """True when the preview has been manually paused."""

    is_capture_orientation_locked: bool
    """True if capture orientation is locked."""

    device_orientation: Optional[ft.DeviceOrientation] = None
    """Current device UI orientation."""

    locked_capture_orientation: Optional[ft.DeviceOrientation] = None
    """Orientation used when capture orientation is locked."""

    recording_orientation: Optional[ft.DeviceOrientation] = None
    """Orientation used for the current recording."""

    preview_pause_orientation: Optional[ft.DeviceOrientation] = None
    """Orientation used when the preview was paused."""

    flash_mode: Optional[FlashMode] = None
    """Active flash mode."""

    exposure_mode: Optional[ExposureMode] = None
    """Active exposure mode."""

    focus_mode: Optional[FocusMode] = None
    """Active focus mode."""

    exposure_point_supported: Optional[bool] = None
    """Whether custom exposure points are supported."""

    focus_point_supported: Optional[bool] = None
    """Whether custom focus points are supported."""

    preview_size: Optional[CameraPreviewSize] = None
    """Preview dimensions, when available."""

    aspect_ratio: Optional[ft.Number] = None
    """Preview aspect ratio, when available."""

    error_description: Optional[str] = None
    """Error message when the controller has an error."""

    has_error: Optional[bool] = None
    """Indicates if the controller is in an error state."""

    description: Optional[CameraDescription] = None
    """The underlying camera description."""


@dataclass
class CameraImageEvent(ft.Event["Camera"]):
    """Image data produced by the camera stream."""

    width: int
    """Pixel width of the frame."""

    height: int
    """Pixel height of the frame."""

    format: Optional[ImageFormatGroup]
    """Raw image format group of the source frame."""

    encoded_format: str
    """Encoding used for the output bytes (e.g., jpeg)."""

    bytes: bytes
    """Encoded image bytes."""

    lens_aperture: Optional[ft.Number] = None
    """Lens aperture value for the frame."""

    sensor_exposure_time: Optional[int] = None
    """Exposure time in nanoseconds."""

    sensor_sensitivity: Optional[ft.Number] = None
    """Sensor sensitivity (ISO)."""
