from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CupertinoActivityIndicator(ConstrainedControl):
    """
    An iOS-style activity indicator that spins clockwise.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactivityindicator
    """

    def __init__(
        self,
        radius: OptionalNumber = None,
        color: Optional[ColorValue] = None,
        animating: Optional[bool] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
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
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.color = color
        self.radius = radius
        self.animating = animating

    def _get_control_name(self):
        return "cupertinoactivityindicator"

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # animating
    @property
    def animating(self) -> bool:
        return self._get_attr("animating", data_type="bool", def_value=True)

    @animating.setter
    def animating(self, value: Optional[bool]):
        self._set_attr("animating", value)

    # radius
    @property
    def radius(self) -> OptionalNumber:
        return self._get_attr("radius", data_type="float")

    @radius.setter
    def radius(self, value: OptionalNumber):
        self._set_attr("radius", value)
