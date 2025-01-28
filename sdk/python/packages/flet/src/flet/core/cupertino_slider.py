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


class CupertinoSlider(ConstrainedControl):
    """
    An iOS-type slider.

    It provides a visual indication of adjustable content, as well as the current setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or brightness), or when people would benefit from instant feedback on the effect of setting changes.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoslider
    """

    def __init__(
        self,
        value: OptionalNumber = None,
        min: OptionalNumber = None,
        max: OptionalNumber = None,
        divisions: Optional[int] = None,
        active_color: Optional[ColorValue] = None,
        thumb_color: Optional[ColorValue] = None,
        on_change: OptionalControlEventCallable = None,
        on_change_start: OptionalControlEventCallable = None,
        on_change_end: OptionalControlEventCallable = None,
        on_focus: OptionalControlEventCallable = None,
        on_blur: OptionalControlEventCallable = None,
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
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.min = min
        self.max = max
        self.divisions = divisions
        self.round = round
        self.active_color = active_color
        self.thumb_color = thumb_color
        self.on_change = on_change
        self.on_change_start = on_change_start
        self.on_change_end = on_change_end
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "cupertinoslider"

    # value
    @property
    def value(self) -> float:
        return self._get_attr("value", data_type="float", def_value=0.0)

    @value.setter
    def value(self, value: OptionalNumber):
        if value is not None:
            if self.min is not None:
                assert value >= self.min, "value must be greater than or equal to min"
            if self.max is not None:
                assert value <= self.max, "value must be less than or equal to max"
        self._set_attr("value", value)

    # min
    @property
    def min(self) -> float:
        return self._get_attr("min", data_type="float", def_value=0.0)

    @min.setter
    def min(self, value: OptionalNumber):
        if value is not None:
            if self.max is not None:
                assert value <= self.max, "min must be less than or equal to max"
        self._set_attr("min", value)

    # max
    @property
    def max(self) -> float:
        return self._get_attr("max", data_type="float", def_value=1.0)

    @max.setter
    def max(self, value: OptionalNumber):
        if value is not None:
            if self.min is not None:
                assert value >= self.min, "max must be greater than or equal to min"
        self._set_attr("max", value)

    # divisions
    @property
    def divisions(self) -> Optional[int]:
        return self._get_attr("divisions", data_type="int")

    @divisions.setter
    def divisions(self, value: Optional[int]):
        self._set_attr("divisions", value)

    # round
    @property
    def round(self) -> int:
        return self._get_attr("round", data_type="int", def_value=0)

    @round.setter
    def round(self, value: Optional[int]):
        self._set_attr("round", value)

    # active_color
    @property
    def active_color(self) -> Optional[ColorValue]:
        return self.__active_color

    @active_color.setter
    def active_color(self, value: Optional[ColorValue]):
        self.__active_color = value
        self._set_enum_attr("activeColor", value, ColorEnums)

    # thumb_color
    @property
    def thumb_color(self) -> Optional[ColorValue]:
        return self.__thumb_color

    @thumb_color.setter
    def thumb_color(self, value: Optional[ColorValue]):
        self.__thumb_color = value
        self._set_enum_attr("thumbColor", value, ColorEnums)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

    # on_change_start
    @property
    def on_change_start(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change_start")

    @on_change_start.setter
    def on_change_start(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change_start", handler)

    # on_change_end
    @property
    def on_change_end(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change_end")

    @on_change_end.setter
    def on_change_end(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change_end", handler)

    # on_focus
    @property
    def on_focus(self) -> OptionalControlEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalControlEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalControlEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalControlEventCallable):
        self._add_event_handler("blur", handler)
