"""
Public exports for the flet-camera package.
"""

from flet_camera.camera import Camera
from flet_camera.types import (
    CameraDescription,
    CameraImageEvent,
    CameraLensDirection,
    CameraLensType,
    CameraPreviewSize,
    CameraStateEvent,
    DeviceOrientation,
    ExposureMode,
    FlashMode,
    FocusMode,
    ImageFormatGroup,
    ResolutionPreset,
)
from flet_camera.utils import detect_video_extension

__all__ = [
    "Camera",
    "CameraDescription",
    "CameraImageEvent",
    "CameraLensDirection",
    "CameraLensType",
    "CameraPreviewSize",
    "CameraStateEvent",
    "DeviceOrientation",
    "ExposureMode",
    "FlashMode",
    "FocusMode",
    "ImageFormatGroup",
    "ResolutionPreset",
    "detect_video_extension",
]
