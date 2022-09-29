from typing import Any, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import BlendMode, OptionalNumber
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


ImageFit = Literal[
    None, "none", "contain", "cover", "fill", "fitHeight", "fitWidth", "scaleDown"
]

ImageRepeat = Literal[None, "noRepeat", "repeat", "repeatX", "repeatY"]


class Image(ConstrainedControl):
    def __init__(
        self,
        src: Optional[str] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        #
        # Specific
        #
        src_base64: Optional[str] = None,
        repeat: ImageRepeat = None,
        fit: ImageFit = None,
        border_radius: BorderRadiusValue = None,
        color: Optional[str] = None,
        color_blend_mode: Optional[BlendMode] = None,
        gapless_playback: Optional[bool] = None,
        semantics_label: Optional[str] = None,
    ):

        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
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
        self.src_base64 = src_base64
        self.fit = fit
        self.repeat = repeat
        self.border_radius = border_radius
        self.color = color
        self.color_blend_mode = color_blend_mode
        self.gapless_playback = gapless_playback
        self.semantics_label = semantics_label

    def _get_control_name(self):
        return "image"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("borderRadius", self.__border_radius)

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value):
        self._set_attr("src", value)

    # src_base64
    @property
    def src_base64(self):
        return self._get_attr("srcBase64")

    @src_base64.setter
    def src_base64(self, value):
        self._set_attr("srcBase64", value)

    # fit
    @property
    def fit(self):
        return self._get_attr("fit")

    @fit.setter
    @beartype
    def fit(self, value: ImageFit):
        self._set_attr("fit", value)

    # repeat
    @property
    def repeat(self):
        return self._get_attr("repeat")

    @repeat.setter
    @beartype
    def repeat(self, value: ImageRepeat):
        self._set_attr("repeat", value)

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # color_blend_mode
    @property
    def color_blend_mode(self) -> Optional[BlendMode]:
        return self._get_attr("colorBlendMode")

    @color_blend_mode.setter
    @beartype
    def color_blend_mode(self, value: Optional[BlendMode]):
        self._set_attr("colorBlendMode", value)

    # gapless_playback
    @property
    def gapless_playback(self) -> Optional[bool]:
        return self._get_attr("gaplessPlayback", data_type="bool", def_value=False)

    @gapless_playback.setter
    @beartype
    def gapless_playback(self, value: Optional[bool]):
        self._set_attr("gaplessPlayback", value)

    # semantics_label
    @property
    def semantics_label(self):
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value):
        self._set_attr("semanticsLabel", value)
