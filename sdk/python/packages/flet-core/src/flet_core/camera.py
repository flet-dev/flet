from enum import Enum
from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber, Control
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class ResolutionPreset(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "veryHigh"
    ULTRA_HIGH = "ultraHigh"
    MAX = "max"


class ImageFormatGroup(Enum):
    UNKNOWN = "unknown"
    YUV420 = "yuv420"
    BGRA8888 = "bgra8888"
    JPEG = "jpeg"
    NV21 = "nv21"


class ExposureMode(Enum):
    LOCKED = "locked"
    AUTO = "auto"


class Camera(ConstrainedControl):
    """
    Camera control.

    -----

    Online docs: https://flet.dev/docs/controls/camera
    """

    def __init__(
        self,
        enable_audio: Optional[bool] = None,
        resolution_preset: Optional[ResolutionPreset] = None,
        image_format_group: Optional[ImageFormatGroup] = None,
        exposure_mode: Optional[ExposureMode] = None,
        exposure_offset: OptionalNumber = None,
        zoom_level: OptionalNumber = None,
        error_content: Optional[Control] = None,
        on_camera_access_denied=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.enable_audio = enable_audio
        self.resolution_preset = resolution_preset
        self.image_format_group = image_format_group
        self.exposure_mode = exposure_mode
        self.exposure_offset = exposure_offset
        self.zoom_level = zoom_level
        self.error_content = error_content
        self.on_camera_access_denied = on_camera_access_denied

    def _get_control_name(self):
        return "camera"

    def _get_children(self):
        children = []
        if self.__error_content is not None:
            self.__error_content._set_attr_internal("n", "error_content")
            children.append(self.__error_content)
        return children

    def capture_image(self):
        self.page.invoke_method("capture_image", control_id=self.uid)

    async def capture_image_async(self):
        await self.page.invoke_method_async("capture_image", control_id=self.uid)

    def start_video_recording(self):
        self.page.invoke_method("start_video_recording", control_id=self.uid)

    def stop_video_recording(self, wait_timeout: Optional[int] = 5):
        return self.page.invoke_method(
            "stop_video_recording",
            control_id=self.uid,
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    async def stop_video_recording_async(self, wait_timeout: Optional[int] = 5):
        return await self.page.invoke_method_async(
            "stop_video_recording",
            control_id=self.uid,
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    # enable_audio
    @property
    def enable_audio(self) -> Optional[bool]:
        return self._get_attr("enableAudio")

    @enable_audio.setter
    def enable_audio(self, value: Optional[bool]):
        self._set_attr("enableAudio", value)

    # resolution_preset
    @property
    def resolution_preset(self) -> Optional[ResolutionPreset]:
        return self.__resolution_preset

    @resolution_preset.setter
    def resolution_preset(self, value: Optional[ResolutionPreset]):
        self.__resolution_preset = value
        self._set_enum_attr("resolutionPreset", value, ResolutionPreset)

    # image_format_group
    @property
    def image_format_group(self) -> Optional[ImageFormatGroup]:
        return self.__image_format_group

    @image_format_group.setter
    def image_format_group(self, value: Optional[ImageFormatGroup]):
        self.__image_format_group = value
        self._set_enum_attr("imageFormatGroup", value, ImageFormatGroup)

    # exposure_mode
    @property
    def exposure_mode(self) -> Optional[ExposureMode]:
        return self.__exposure_mode

    @exposure_mode.setter
    def exposure_mode(self, value: Optional[ExposureMode]):
        self.__exposure_mode = value
        self._set_enum_attr("exposureMode", value, ExposureMode)

    # exposure_offset
    @property
    def exposure_offset(self) -> OptionalNumber:
        return self._get_attr("exposureOffset", data_type="float")

    @exposure_offset.setter
    def exposure_offset(self, value: OptionalNumber):
        self._set_attr("exposureOffset", value)

    # zoom_level
    @property
    def zoom_level(self) -> OptionalNumber:
        return self._get_attr("zoomLevel", data_type="float")

    @zoom_level.setter
    def zoom_level(self, value: OptionalNumber):
        self._set_attr("zoomLevel", value)

    # error_content
    @property
    def error_content(self) -> Optional[Control]:
        return self.__error_content

    @error_content.setter
    def error_content(self, value: Optional[Control]):
        self.__error_content = value

    # on_camera_access_denied
    @property
    def on_camera_access_denied(self):
        return self._get_event_handler("cameraAccessDenied")

    @on_camera_access_denied.setter
    def on_camera_access_denied(self, handler):
        self._add_event_handler("cameraAccessDenied", handler)
        self._set_attr("onCameraAccessDenied", True if handler is not None else None)
