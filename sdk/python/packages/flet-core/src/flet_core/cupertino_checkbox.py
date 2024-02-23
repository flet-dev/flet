from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    LabelPosition,
    OffsetValue,
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
        label_position: LabelPosition = LabelPosition.NONE,
        value: Optional[bool] = None,
        tristate: Optional[bool] = None,
        autofocus: Optional[bool] = None,
        check_color: Optional[str] = None,
        active_color: Optional[str] = None,
        inactive_color: Optional[str] = None,
        focus_color: Optional[str] = None,
        on_change=None,
        on_focus=None,
        on_blur=None,
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
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

    def _get_control_name(self):
        return "cupertinocheckbox"

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
    def tristate(self) -> Optional[bool]:
        return self._get_attr("tristate", data_type="bool", def_value=False)

    @tristate.setter
    def tristate(self, value: Optional[bool]):
        self._set_attr("tristate", value)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # label_position
    @property
    def label_position(self) -> LabelPosition:
        return self.__label_position

    @label_position.setter
    def label_position(self, value: LabelPosition):
        self.__label_position = value
        self._set_attr(
            "labelPosition", value.value if isinstance(value, LabelPosition) else value
        )

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # check_color
    @property
    def check_color(self):
        return self._get_attr("checkColor")

    @check_color.setter
    def check_color(self, value):
        self._set_attr("checkColor", value)

    # active_color
    @property
    def active_color(self):
        return self._get_attr("activeColor")

    @active_color.setter
    def active_color(self, value):
        self._set_attr("activeColor", value)

    # inactive_color
    @property
    def inactive_color(self):
        return self._get_attr("inactiveColor")

    @inactive_color.setter
    def inactive_color(self, value):
        self._set_attr("inactiveColor", value)

    # focus_color
    @property
    def focus_color(self):
        return self._get_attr("focusColor")

    @focus_color.setter
    def focus_color(self, value):
        self._set_attr("focusColor", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # on_focus
    @property
    def on_focus(self):
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self):
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler):
        self._add_event_handler("blur", handler)
