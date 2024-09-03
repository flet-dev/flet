from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
)


class Placeholder(ConstrainedControl):
    """
    A placeholder box.

    -----

    Online docs: https://flet.dev/docs/controls/placeholder
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        color: Optional[str] = None,
        fallback_height: OptionalNumber = None,
        fallback_width: OptionalNumber = None,
        stroke_width: OptionalNumber = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
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

        self.content = content
        self.color = color
        self.fallback_height = fallback_height
        self.fallback_width = fallback_width
        self.stroke_width = stroke_width

    def _get_control_name(self):
        return "placeholder"

    def _get_children(self):
        return [self.content] if self.content is not None else []

    # fallback_height
    @property
    def fallback_height(self) -> float:
        return self._get_attr("fallbackHeight", data_type="float", def_value=400.0)

    @fallback_height.setter
    def fallback_height(self, value: OptionalNumber):
        assert value is None or value >= 0, "fallback_height cannot be negative"
        self._set_attr("fallbackHeight", value)

    # fallback_width
    @property
    def fallback_width(self) -> float:
        return self._get_attr("fallbackWidth", data_type="float", def_value=400.0)

    @fallback_width.setter
    def fallback_width(self, value: OptionalNumber):
        assert value is None or value >= 0, "fallback_width cannot be negative"
        self._set_attr("fallbackWidth", value)

    # stroke_width
    @property
    def stroke_width(self) -> float:
        return self._get_attr("strokeWidth", data_type="float", def_value=2.0)

    @stroke_width.setter
    def stroke_width(self, value: OptionalNumber):
        self._set_attr("strokeWidth", value)

    # color
    @property
    def color(self) -> str:
        return self._get_attr("color", def_value="bluegrey700")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value
