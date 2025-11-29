from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional, TypeVar

import flet as ft

if TYPE_CHECKING:
    from flet_camera.camera import Camera  # noqa

__all__ = [
    "CameraDescription",
    "CameraImage",
    "CameraLensDirection",
    "CameraLensType",
    "CameraPreviewSize",
    "CameraState",
    "DeviceOrientation",
    "ExposureMode",
    "FlashMode",
    "FocusMode",
    "ImageFormatGroup",
    "ResolutionPreset",
]


class ResolutionPreset(Enum):
    """Represents a capture resolution preset."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "veryHigh"
    ULTRA_HIGH = "ultraHigh"
    MAX = "max"


class ImageFormatGroup(Enum):
    """Describes the image output format."""

    BGRA8888 = "bgra8888"
    JPEG = "jpeg"
    NV21 = "nv21"
    YUV420 = "yuv420"
    UNKNOWN = "unknown"


class FlashMode(Enum):
    """Flash modes supported by the camera."""

    OFF = "off"
    AUTO = "auto"
    ALWAYS = "always"
    TORCH = "torch"


class ExposureMode(Enum):
    """Exposure modes supported by the camera."""

    AUTO = "auto"
    LOCKED = "locked"


class FocusMode(Enum):
    """Focus modes supported by the camera."""

    AUTO = "auto"
    LOCKED = "locked"


class CameraLensDirection(Enum):
    """Direction the camera is facing."""

    FRONT = "front"
    BACK = "back"
    EXTERNAL = "external"


class CameraLensType(Enum):
    """Type of the camera lens."""

    WIDE = "wide"
    TELEPHOTO = "telephoto"
    ULTRA_WIDE = "ultraWide"
    UNKNOWN = "unknown"


class DeviceOrientation(Enum):
    """Device orientation values."""

    PORTRAIT_UP = "portraitUp"
    PORTRAIT_DOWN = "portraitDown"
    LANDSCAPE_LEFT = "landscapeLeft"
    LANDSCAPE_RIGHT = "landscapeRight"


_EnumT = TypeVar("_EnumT", bound=Enum)


@dataclass
class CameraPreviewSize:
    """Dimensions of a camera preview."""

    width: ft.Number
    height: ft.Number


@dataclass
class CameraDescription:
    """Properties of a camera device."""

    name: str
    lens_direction: CameraLensDirection
    sensor_orientation: int
    lens_type: CameraLensType = CameraLensType.UNKNOWN


@dataclass
class CameraState(ft.Event["Camera"]):
    """Snapshot of the camera controller state."""

    is_initialized: bool
    is_recording_video: bool
    is_recording_paused: bool
    is_taking_picture: bool
    is_streaming_images: bool
    is_preview_paused: bool
    is_capture_orientation_locked: bool
    device_orientation: Optional[DeviceOrientation] = None
    locked_capture_orientation: Optional[DeviceOrientation] = None
    recording_orientation: Optional[DeviceOrientation] = None
    preview_pause_orientation: Optional[DeviceOrientation] = None
    flash_mode: Optional[FlashMode] = None
    exposure_mode: Optional[ExposureMode] = None
    focus_mode: Optional[FocusMode] = None
    exposure_point_supported: Optional[bool] = None
    focus_point_supported: Optional[bool] = None
    preview_size: Optional[CameraPreviewSize] = None
    aspect_ratio: Optional[ft.Number] = None
    error_description: Optional[str] = None
    has_error: Optional[bool] = None
    description: Optional[CameraDescription] = None


@dataclass
class CameraImage(ft.Event["Camera"]):
    """Image data produced by the camera stream."""

    width: int
    height: int
    format: Optional[ImageFormatGroup]
    encoded_format: str
    bytes: bytes
    lens_aperture: Optional[ft.Number] = None
    sensor_exposure_time: Optional[int] = None
    sensor_sensitivity: Optional[ft.Number] = None
