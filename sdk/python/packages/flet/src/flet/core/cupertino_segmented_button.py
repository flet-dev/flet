from typing import Any, List, Optional, Sequence, Union

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


class CupertinoSegmentedButton(ConstrainedControl):
    """
    An iOS-style segmented button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinosegmentedbutton
    """

    def __init__(
        self,
        controls: Sequence[Control],
        selected_index: Optional[int] = None,
        selected_color: Optional[ColorValue] = None,
        unselected_color: Optional[ColorValue] = None,
        border_color: Optional[ColorValue] = None,
        padding: Optional[PaddingValue] = None,
        click_color: Optional[ColorValue] = None,
        disabled_color: Optional[ColorValue] = None,
        disabled_text_color: Optional[ColorValue] = None,
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
        self.border_color = border_color
        self.selected_index = selected_index
        self.selected_color = selected_color
        self.unselected_color = unselected_color
        self.on_change = on_change
        self.click_color = click_color
        self.disabled_color = disabled_color
        self.disabled_text_color = disabled_text_color

    def _get_control_name(self):
        return "cupertinosegmentedbutton"

    def _get_children(self):
        return self.__controls

    def before_update(self):
        super().before_update()
        assert (
            len(self.__controls) >= 2
        ), "CupertinoSegmentedButton must have at minimum two visible controls"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("padding", self.__padding)

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    @controls.setter
    def controls(self, value: Sequence[Control]):
        self.__controls = list(value)

    # border_color
    @property
    def border_color(self) -> Optional[ColorValue]:
        return self.__border_color

    @border_color.setter
    def border_color(self, value: Optional[ColorValue]):
        self.__border_color = value
        self._set_enum_attr("borderColor", value, ColorEnums)

    # disabled_color
    @property
    def disabled_color(self) -> Optional[ColorValue]:
        return self.__disabled_color

    @disabled_color.setter
    def disabled_color(self, value: Optional[ColorValue]):
        self.__disabled_color = value
        self._set_enum_attr("disabledColor", value, ColorEnums)

    # disabled_text_color
    @property
    def disabled_text_color(self) -> Optional[ColorValue]:
        return self.__disabled_text_color

    @disabled_text_color.setter
    def disabled_text_color(self, value: Optional[ColorValue]):
        self.__disabled_text_color = value
        self._set_enum_attr("disabledTextColor", value, ColorEnums)

    # selected_index
    @property
    def selected_index(self) -> int:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        if value is not None and not (0 <= value < len(self.controls)):
            raise IndexError("selected_index out of range")
        self._set_attr("selectedIndex", value)

    # selected_color
    @property
    def selected_color(self) -> Optional[ColorValue]:
        return self.__selected_color

    @selected_color.setter
    def selected_color(self, value: Optional[ColorValue]):
        self.__selected_color = value
        self._set_enum_attr("selectedColor", value, ColorEnums)

    # unselected_color
    @property
    def unselected_color(self) -> Optional[ColorValue]:
        return self.__unselected_color

    @unselected_color.setter
    def unselected_color(self, value: Optional[ColorValue]):
        self.__unselected_color = value
        self._set_enum_attr("unselectedColor", value, ColorEnums)

    # click_color
    @property
    def click_color(self) -> Optional[ColorValue]:
        return self.__click_color

    @click_color.setter
    def click_color(self, value: Optional[ColorValue]):
        self.__click_color = value
        self._set_enum_attr("clickColor", value, ColorEnums)

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
