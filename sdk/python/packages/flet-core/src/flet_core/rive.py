from typing import Any, Optional, Union

from flet_core.alignment import Alignment
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber, Control
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


class Rive(ConstrainedControl):
    """
    Displays rive animations.

    -----

    Online docs: https://flet.dev/docs/controls/rive
    """

    def __init__(
        self,
        src: str,
        placeholder: Optional[Control] = None,
        artboard: Optional[str] = None,
        alignment: Optional[Alignment] = None,
        enable_antialiasing: Optional[bool] = None,
        use_artboard_size: Optional[bool] = None,
        fit: Optional[ImageFit] = None,
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
        self.placeholder = placeholder
        self.artboard = artboard
        self.enable_antialiasing = enable_antialiasing
        self.use_artboard_size = use_artboard_size
        self.alignment = alignment
        self.fit = fit

    def _get_control_name(self):
        return "rive"

    def before_update(self):
        super().before_update()
        assert self.src, "src must be provided"
        self._set_attr_json("alignment", self.__alignment)

    def _get_children(self):
        if self.__placeholder:
            return [self.__placeholder]
        return []

    # src
    @property
    def src(self) -> Optional[str]:
        return self._get_attr("src")

    @src.setter
    def src(self, value: Optional[str]):
        self._set_attr("src", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # artboard
    @property
    def artboard(self):
        return self._get_attr("artBoard")

    @artboard.setter
    def artboard(self, value):
        self._set_attr("artBoard", value)

    # enable_antialiasing
    @property
    def enable_antialiasing(self) -> Optional[bool]:
        return self._get_attr("enableAntiAliasing", def_value=True, data_type="bool")

    @enable_antialiasing.setter
    def enable_antialiasing(self, value: Optional[bool]):
        self._set_attr("enableAntiAliasing", value)

    # placeholder
    @property
    def placeholder(self) -> Optional[Control]:
        return self.__placeholder

    @placeholder.setter
    def placeholder(self, value: Optional[Control]):
        self.__placeholder = value

    # use_artboard_size
    @property
    def use_artboard_size(self) -> Optional[bool]:
        return self._get_attr("useArtBoardSize", def_value=False, data_type="bool")

    @use_artboard_size.setter
    def use_artboard_size(self, value: Optional[bool]):
        self._set_attr("useArtBoardSize", value)

    # fit
    @property
    def fit(self) -> Optional[ImageFit]:
        return self.__fit

    @fit.setter
    def fit(self, value: Optional[ImageFit]):
        self.__fit = value
        self._set_enum_attr("fit", value, ImageFit)
