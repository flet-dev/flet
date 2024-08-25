from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    LabelPosition,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
)


class CupertinoSwitch(ConstrainedControl):
    """
    An iOS-style switch. Used to toggle the on/off state of a single setting.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.CupertinoSwitch(label="Cupertino Switch", value=True),
            ft.Switch(label="Material Checkbox", value=True),
            ft.Container(height=20),
            ft.Text(
                "Adaptive Switch shows as CupertinoSwitch on macOS and iOS and as Switch on other platforms:"
            ),
            ft.Switch(adaptive=True, label="Adaptive Switch", value=True),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/cupertinoswitch
    """

    def __init__(
        self,
        label: Optional[str] = None,
        value: Optional[bool] = None,
        label_position: Optional[LabelPosition] = None,
        active_color: Optional[str] = None,
        thumb_color: Optional[str] = None,
        track_color: Optional[str] = None,
        focus_color: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_label_color: Optional[str] = None,
        off_label_color: Optional[str] = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
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
        self.label = label
        self.label_position = label_position
        self.autofocus = autofocus
        self.active_color = active_color
        self.focus_color = focus_color
        self.thumb_color = thumb_color
        self.track_color = track_color
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.on_label_color = on_label_color
        self.off_label_color = off_label_color

    def _get_control_name(self):
        return "cupertinoswitch"

    def before_update(self):
        super().before_update()
        self._set_attr_json("thumbColor", self.__thumb_color)
        self._set_attr_json("trackColor", self.__track_color)

    # value
    @property
    def value(self) -> bool:
        return self._get_attr("value", data_type="bool", def_value=False)

    @value.setter
    def value(self, value: Optional[bool]):
        self._set_attr("value", value)

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

    # active_color
    @property
    def active_color(self) -> Optional[str]:
        return self._get_attr("activeColor")

    @active_color.setter
    def active_color(self, value: Optional[str]):
        self._set_attr("activeColor", value)

    # focus_color
    @property
    def focus_color(self) -> Optional[str]:
        return self._get_attr("focusColor")

    @focus_color.setter
    def focus_color(self, value: Optional[str]):
        self._set_attr("focusColor", value)

    # thumb_color
    @property
    def thumb_color(self) -> Optional[str]:
        return self.__thumb_color

    @thumb_color.setter
    def thumb_color(self, value: Optional[str]):
        self.__thumb_color = value

    # track_color
    @property
    def track_color(self) -> Optional[str]:
        return self.__track_color

    @track_color.setter
    def track_color(self, value: Optional[str]):
        self.__track_color = value

    # on_label_color
    @property
    def on_label_color(self) -> Optional[str]:
        return self._get_attr("onLabelColor")

    @on_label_color.setter
    def on_label_color(self, value: Optional[str]):
        self._set_attr("onLabelColor", value)

    # off_label_color
    @property
    def off_label_color(self) -> Optional[str]:
        return self._get_attr("offLabelColor")

    @off_label_color.setter
    def off_label_color(self, value: Optional[str]):
        self._set_attr("offLabelColor", value)

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
