from typing import Any, Optional, Union

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
    OptionalEventCallable,
)
from flet_core.video import FilterQuality


class Lottie(ConstrainedControl):
    """
    Displays lottie animations.

    -----

    Online docs: https://flet.dev/docs/controls/lottie
    """

    def __init__(
        self,
        src: Optional[str] = None,
        src_base64: Optional[str] = None,
        repeat: Optional[bool] = None,
        reverse: Optional[bool] = None,
        animate: Optional[bool] = None,
        background_loading: Optional[bool] = None,
        filter_quality: Optional[FilterQuality] = None,
        fit: Optional[ImageFit] = None,
        on_error=None,
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
        expand_loose: Optional[bool] = None,
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
            on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
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
            expand_loose=expand_loose,
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
            rtl=rtl,
        )

        self.src = src
        self.src_base64 = src_base64
        self.repeat = repeat
        self.reverse = reverse
        self.animate = animate
        self.filter_quality = filter_quality
        self.fit = fit
        self.background_loading = background_loading
        self.on_error = on_error

    def _get_control_name(self):
        return "lottie"

    # src
    @property
    def src(self) -> Optional[str]:
        return self._get_attr("src")

    @src.setter
    def src(self, value: Optional[str]):
        self._set_attr("src", value)

    # src_base64
    @property
    def src_base64(self) -> Optional[str]:
        return self._get_attr("srcBase64")

    @src_base64.setter
    def src_base64(self, value: Optional[str]):
        self._set_attr("srcBase64", value)

    # repeat
    @property
    def repeat(self) -> Optional[bool]:
        return self._get_attr("repeat", def_value=True, data_type="bool")

    @repeat.setter
    def repeat(self, value: Optional[bool]):
        self._set_attr("repeat", value)

    # animate
    @property
    def animate(self) -> Optional[bool]:
        return self._get_attr("animate", def_value=True, data_type="bool")

    @animate.setter
    def animate(self, value: Optional[bool]):
        self._set_attr("animate", value)

    # reverse
    @property
    def reverse(self) -> Optional[bool]:
        return self._get_attr("reverse", def_value=False, data_type="bool")

    @reverse.setter
    def reverse(self, value: Optional[bool]):
        self._set_attr("reverse", value)

    # filter_quality
    @property
    def filter_quality(self) -> Optional[FilterQuality]:
        return self.__filter_quality

    @filter_quality.setter
    def filter_quality(self, value: Optional[FilterQuality]):
        self.__filter_quality = value
        self._set_enum_attr("filterQuality", value, FilterQuality)

    # fit
    @property
    def fit(self) -> Optional[ImageFit]:
        return self.__fit

    @fit.setter
    def fit(self, value: Optional[ImageFit]):
        self.__fit = value
        self._set_enum_attr("fit", value, ImageFit)

    # background_loading
    @property
    def background_loading(self) -> Optional[bool]:
        return self._get_attr("backgroundLoading", data_type="bool")

    @background_loading.setter
    def background_loading(self, value: Optional[bool]):
        self._set_attr("backgroundLoading", value)

    # on_error
    @property
    def on_error(self) -> OptionalEventCallable:
        return self._get_event_handler("error")

    @on_error.setter
    def on_error(self, handler: OptionalEventCallable):
        self._add_event_handler("error", handler)
        self._set_attr("onError", True if handler is not None else None)
