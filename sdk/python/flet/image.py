from sys import version
from typing import Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
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
except:
    from typing_extensions import Literal


ImageFit = Literal[
    None, "none", "contain", "cover", "fill", "fitHeight", "fitWidth", "scaleDown"
]

ImageRepeat = Literal[None, "noRepeat", "repeat", "repeatX", "repeatY"]


class Image(ConstrainedControl):
    def __init__(
        self,
        src: str = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[bool, int] = None,
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
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        src_base64: bool = None,
        repeat: ImageRepeat = None,
        fit: ImageFit = None,
        border_radius: BorderRadiusValue = None,
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
    def border_radius(self):
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value
