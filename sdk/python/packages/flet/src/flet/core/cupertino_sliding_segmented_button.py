from typing import Any, Optional, Sequence, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CupertinoSlidingSegmentedButton(ConstrainedControl):
    """

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoslidingsegmentedbutton
    """

    def __init__(
        self,
        controls: Sequence[Control],
        selected_index: Optional[int] = None,
        bgcolor: Optional[ColorValue] = None,
        thumb_color: Optional[ColorValue] = None,
        padding: Optional[PaddingValue] = None,
        proportional_width: Optional[bool] = None,
        on_change: OptionalControlEventCallable = None,
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
        self.controls = controls
        self.padding = padding
        self.selected_index = selected_index
        self.bgcolor = bgcolor
        self.thumb_color = thumb_color
        self.on_change = on_change
        self.proportional_width = proportional_width

    def _get_control_name(self):
        return "cupertinoslidingsegmentedbutton"

    def _get_children(self):
        return self.__controls

    def before_update(self):
        super().before_update()
        assert (
            len(self.__controls) >= 2
        ), "CupertinoSlidingSegmentedButton must have at minimum two visible controls"
        self._set_attr_json("padding", self.__padding)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Sequence[Control]):
        self.__controls = list(value)

    # selected_index
    @property
    def selected_index(self) -> int:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        assert (
            value is None or 0 <= value <= len(self.controls) - 1
        ), "selected_index out of range"
        self._set_attr("selectedIndex", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # proportional_width

    @property
    def proportional_width(self) -> Optional[bool]:
        return self._get_attr("proportionalWidth", data_type="bool", def_value=False)

    @proportional_width.setter
    def proportional_width(self, value: Optional[bool]):
        self._set_attr("proportionalWidth", value)

    # thumb_color
    @property
    def thumb_color(self) -> Optional[ColorValue]:
        return self.__thumb_color

    @thumb_color.setter
    def thumb_color(self, value: Optional[ColorValue]):
        self.__thumb_color = value
        self._set_enum_attr("thumbColor", value, ColorEnums)

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
