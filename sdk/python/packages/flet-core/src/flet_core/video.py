from enum import Enum
from typing import Any, Optional, Union, List

from flet_core.alignment import Alignment
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ImageFit,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class FilterQuality(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Video(ConstrainedControl):
    """
    A video widget.

    -----

    Online docs: https://flet.dev/docs/controls/video
    """

    def __init__(
        self,
        sources: Optional[List[str]] = None,  # TODO
        fit: Optional[ImageFit] = None,
        fill_color: Optional[str] = None,
        wakelock: Optional[bool] = None,
        autoplay: Optional[bool] = None,
        alignment: Optional[Alignment] = None,
        filter_quality: Optional[FilterQuality] = None,
        pause_upon_entering_background_mode: Optional[bool] = None,
        resume_upon_entering_foreground_mode: Optional[bool] = None,
        aspect_ratio: OptionalNumber = None,
        on_enter_fullscreen=None,
        on_exit_fullscreen=None,
        #
        # Common
        #
        src: Optional[str] = None,
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

        self.src = src
        self.fit = fit
        self.fill_color = fill_color
        self.alignment = alignment
        self.wakelock = wakelock
        self.autoplay = autoplay
        self.pause_upon_entering_background_mode = pause_upon_entering_background_mode
        self.resume_upon_entering_foreground_mode = resume_upon_entering_foreground_mode
        self.on_enter_fullscreen = on_enter_fullscreen
        self.on_exit_fullscreen = on_exit_fullscreen
        self.filter_quality = filter_quality

    def _get_control_name(self):
        return "video"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("alignment", self.__alignment)

    def play(self):
        self.page.invoke_method("play", control_id=self.uid)

    async def play_async(self):
        await self.page.invoke_method_async("play", control_id=self.uid)

    def pause(self):
        self.page.invoke_method("pause", control_id=self.uid)

    async def pause_async(self):
        await self.page.invoke_method_async("pause", control_id=self.uid)

    def play_or_pause(self):
        self.page.invoke_method("play_or_pause", control_id=self.uid)

    async def play_or_pause_async(self):
        await self.page.invoke_method_async("play_or_pause", control_id=self.uid)

    def stop(self):
        self.page.invoke_method("stop", control_id=self.uid)

    async def stop_async(self):
        await self.page.invoke_method_async("stop", control_id=self.uid)

    def next(self):
        self.page.invoke_method("next", control_id=self.uid)

    async def next_async(self):
        await self.page.invoke_method_async("next", control_id=self.uid)

    def previous(self):
        self.page.invoke_method("previous", control_id=self.uid)

    async def previous_async(self):
        await self.page.invoke_method_async("previous", control_id=self.uid)

    def seek(self, position_milliseconds: int):
        self.page.invoke_method(
            "seek", {"position": str(position_milliseconds)}, control_id=self.uid
        )

    async def seek_async(self, position_milliseconds: int):
        await self.page.invoke_method_async(
            "seek", {"position": str(position_milliseconds)}, control_id=self.uid
        )

    # fit
    @property
    def fit(self) -> Optional[ImageFit]:
        return self.__fit

    @fit.setter
    def fit(self, value: Optional[ImageFit]):
        self.__fit = value
        self._set_attr("fit", value.value if isinstance(value, ImageFit) else value)

    # fill_color
    @property
    def fill_color(self):
        return self._get_attr("fillColor")

    @fill_color.setter
    def fill_color(self, value):
        self._set_attr("fillColor", value)

    # wakelock
    @property
    def wakelock(self) -> Optional[bool]:
        return self._get_attr("wakelock", data_type="bool", def_value=True)

    @wakelock.setter
    def wakelock(self, value: Optional[bool]):
        self._set_attr("wakelock", value)

    # autoplay
    @property
    def autoplay(self) -> Optional[bool]:
        return self._get_attr("autoplay", data_type="bool", def_value=False)

    @autoplay.setter
    def autoplay(self, value: Optional[bool]):
        self._set_attr("autoplay", value)

    # pause_upon_entering_background_mode
    @property
    def pause_upon_entering_background_mode(self) -> Optional[bool]:
        return self._get_attr(
            "pauseUponEnteringBackgroundMode", data_type="bool", def_value=True
        )

    @pause_upon_entering_background_mode.setter
    def pause_upon_entering_background_mode(self, value: Optional[bool]):
        self._set_attr("pauseUponEnteringBackgroundMode", value)

    # resume_upon_entering_foreground_mode
    @property
    def resume_upon_entering_foreground_mode(self) -> Optional[bool]:
        return self._get_attr(
            "resumeUponEnteringForegroundMode", data_type="bool", def_value=False
        )

    @resume_upon_entering_foreground_mode.setter
    def resume_upon_entering_foreground_mode(self, value: Optional[bool]):
        self._set_attr("resumeUponEnteringForegroundMode", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # filter_quality
    @property
    def filter_quality(self) -> Optional[FilterQuality]:
        return self.__filter_quality

    @filter_quality.setter
    def filter_quality(self, value: Optional[FilterQuality]):
        self.__filter_quality = value
        self._set_attr(
            "filterQuality", value.value if isinstance(value, FilterQuality) else value
        )

    # on_enter_fullscreen
    @property
    def on_enter_fullscreen(self):
        return self._get_event_handler("enter_fullscreen")

    @on_enter_fullscreen.setter
    def on_enter_fullscreen(self, handler):
        self._add_event_handler("enter_fullscreen", handler)
        self._set_attr("onEnterFullscreen", True if handler is not None else None)

    # on_exit_fullscreen
    @property
    def on_exit_fullscreen(self):
        return self._get_event_handler("exit_fullscreen")

    @on_exit_fullscreen.setter
    def on_exit_fullscreen(self, handler):
        self._add_event_handler("exit_fullscreen", handler)
        self._set_attr("onExitFullscreen", True if handler is not None else None)
