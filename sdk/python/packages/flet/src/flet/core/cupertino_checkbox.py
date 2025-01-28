from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.border import BorderSide
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    ControlStateValue,
    LabelPosition,
    MouseCursor,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CupertinoCheckbox(ConstrainedControl):
    """
    A macOS style checkbox. Checkbox allows to select one or more items from a group, or switch between two mutually exclusive options (checked or unchecked, on or off).

    Example:
    ```
    import flet as ft

    def main(page):
        c = ft.CupertinoCheckbox(
            label="Cupertino Checkbox",
            active_color=ft.colors.GREEN,
            inactive_color=ft.colors.RED,
            check_color=ft.colors.BLUE,
        ),
        page.add(c)

    ft.app(target=main)
    ```

    -----
    Online docs: https://flet.dev/docs/controls/cupertinocheckbox
    """

    def __init__(
        self,
        label: Optional[str] = None,
        label_position: Optional[LabelPosition] = None,
        value: Optional[bool] = None,
        tristate: Optional[bool] = None,
        autofocus: Optional[bool] = None,
        check_color: Optional[ColorValue] = None,
        active_color: Optional[ColorValue] = None,
        inactive_color: Optional[ColorValue] = None,
        focus_color: Optional[ColorValue] = None,
        fill_color: ControlStateValue[ColorValue] = None,
        shape: Optional[OutlinedBorder] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        semantics_label: Optional[str] = None,
        border_side: ControlStateValue[BorderSide] = None,
        on_change: OptionalControlEventCallable = None,
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
        self.tristate = tristate
        self.label = label
        self.label_position = label_position
        self.autofocus = autofocus
        self.check_color = check_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.focus_color = focus_color
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.shape = shape
        self.mouse_cursor = mouse_cursor
        self.semantics_label = semantics_label
        self.border_side = border_side
        self.fill_color = fill_color

    def _get_control_name(self):
        return "cupertinocheckbox"

    def before_update(self):
        super().before_update()
        self._set_attr_json("shape", self.__shape)
        self._set_attr_json("borderSide", self.__border_side, wrap_attr_dict=True)
        self._set_attr_json("fillColor", self.__fill_color, wrap_attr_dict=True)

    # value
    @property
    def value(self) -> Optional[bool]:
        return self._get_attr(
            "value", data_type="bool?", def_value=False if not self.tristate else None
        )

    @value.setter
    def value(self, value: Optional[bool]):
        self._set_attr("value", value)

    # tristate
    @property
    def tristate(self) -> bool:
        return self._get_attr("tristate", data_type="bool", def_value=False)

    @tristate.setter
    def tristate(self, value: Optional[bool]):
        self._set_attr("tristate", value)

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # label_position
    @property
    def label_position(self) -> Optional[LabelPosition]:
        return self.__label_position

    @label_position.setter
    def label_position(self, value: Optional[LabelPosition]):
        self.__label_position = value
        self._set_enum_attr("labelPosition", value, LabelPosition)

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # check_color
    @property
    def check_color(self) -> Optional[ColorValue]:
        return self.__check_color

    @check_color.setter
    def check_color(self, value: Optional[ColorValue]):
        self.__check_color = value
        self._set_enum_attr("checkColor", value, ColorEnums)

    # active_color
    @property
    def active_color(self) -> Optional[ColorValue]:
        return self.__active_color

    @active_color.setter
    def active_color(self, value: Optional[ColorValue]):
        self.__active_color = value
        self._set_enum_attr("activeColor", value, ColorEnums)

    # inactive_color
    @property
    def inactive_color(self) -> Optional[ColorValue]:
        return self.__inactive_color

    @inactive_color.setter
    def inactive_color(self, value: Optional[ColorValue]):
        self.__inactive_color = value
        self._set_enum_attr("inactiveColor", value, ColorEnums)

    # focus_color
    @property
    def focus_color(self) -> Optional[ColorValue]:
        return self.__focus_color

    @focus_color.setter
    def focus_color(self, value: Optional[ColorValue]):
        self.__focus_color = value
        self._set_enum_attr("focusColor", value, ColorEnums)

    # fill_color
    @property
    def fill_color(self) -> ControlStateValue[ColorValue]:
        return self.__fill_color

    @fill_color.setter
    def fill_color(self, value: ControlStateValue[ColorValue]):
        self.__fill_color = value

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # border_side
    @property
    def border_side(self) -> ControlStateValue[BorderSide]:
        return self.__border_side

    @border_side.setter
    def border_side(self, value: ControlStateValue[BorderSide]):
        self.__border_side = value

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

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
