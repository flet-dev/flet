from enum import Enum
from typing import Any, Dict, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    ControlState,
    MouseCursor,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
)


class SliderInteraction(Enum):
    TAP_AND_SLIDE = "tapAndSlide"
    TAP_ONLY = "tapOnly"
    SLIDE_ONLY = "slideOnly"
    SLIDE_THUMB = "slideThumb"


class Slider(ConstrainedControl, AdaptiveControl):
    """
    A slider provides a visual indication of adjustable content, as well as the current setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or brightness), or when people would benefit from instant feedback on the effect of setting changes.

    Example:
    ```
    import flet as ft

    def main(page):
        page.add(
            ft.Text("Slider with value:"),
            ft.Slider(value=0.3),
            ft.Text("Slider with a custom range and label:"),
            ft.Slider(min=0, max=100, divisions=10, label="{value}%"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/slider
    """

    def __init__(
        self,
        value: OptionalNumber = None,
        label: Optional[str] = None,
        min: OptionalNumber = None,
        max: OptionalNumber = None,
        divisions: Optional[int] = None,
        round: Optional[int] = None,
        autofocus: Optional[bool] = None,
        active_color: Optional[str] = None,
        inactive_color: Optional[str] = None,
        thumb_color: Optional[str] = None,
        interaction: Optional[SliderInteraction] = None,
        secondary_active_color: Optional[str] = None,
        overlay_color: Union[None, str, Dict[ControlState, str]] = None,
        secondary_track_value: OptionalNumber = None,
        mouse_cursor: Optional[MouseCursor] = None,
        on_change: OptionalEventCallable = None,
        on_change_start: OptionalEventCallable = None,
        on_change_end: OptionalEventCallable = None,
        on_focus: OptionalEventCallable = None,
        on_blur: OptionalEventCallable = None,
        #
        # ConstrainedControl and AdaptiveControl
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
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = None,
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

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.value = value
        self.label = label
        self.min = min
        self.max = max
        self.divisions = divisions
        self.round = round
        self.autofocus = autofocus
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.thumb_color = thumb_color
        self.interaction = interaction
        self.overlay_color = overlay_color
        self.on_change = on_change
        self.on_change_start = on_change_start
        self.on_change_end = on_change_end
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.secondary_active_color = secondary_active_color
        self.secondary_track_value = secondary_track_value
        self.mouse_cursor = mouse_cursor

    def _get_control_name(self):
        return "slider"

    def before_update(self):
        super().before_update()
        assert (
            self.min is None or self.max is None or self.min <= self.max
        ), "min must be less than or equal to max"
        assert (
            self.min is None or self.value is None or (self.value >= self.min)
        ), "value must be greater than or equal to min"
        assert (
            self.max is None or self.value is None or (self.value <= self.max)
        ), "value must be less than or equal to max"
        self._set_attr_json("overlayColor", self.__overlay_color)

    # value
    @property
    def value(self) -> OptionalNumber:
        return self._get_attr("value", data_type="float", def_value=self.min or 0)

    @value.setter
    def value(self, value: OptionalNumber):
        self._set_attr("value", value)

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # interaction
    @property
    def interaction(self) -> Optional[SliderInteraction]:
        return self.__interaction

    @interaction.setter
    def interaction(self, value: Optional[SliderInteraction]):
        self.__interaction = value
        self._set_enum_attr("interaction", value, SliderInteraction)

    # min
    @property
    def min(self) -> OptionalNumber:
        return self._get_attr("min", data_type="float", def_value=0)

    @min.setter
    def min(self, value: OptionalNumber):
        self._set_attr("min", value)

    # secondary_track_value
    @property
    def secondary_track_value(self) -> OptionalNumber:
        return self._get_attr("secondaryTrackValue", data_type="float")

    @secondary_track_value.setter
    def secondary_track_value(self, value: OptionalNumber):
        self._set_attr("secondaryTrackValue", value)

    # secondary_active_color
    @property
    def secondary_active_color(self) -> Optional[str]:
        return self._get_attr("secondaryActiveColor")

    @secondary_active_color.setter
    def secondary_active_color(self, value: Optional[str]):
        self._set_attr("secondaryActiveColor", value)

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self._get_attr("mouseCursor")

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # max
    @property
    def max(self) -> OptionalNumber:
        return self._get_attr("max", data_type="float", def_value=1)

    @max.setter
    def max(self, value: OptionalNumber):
        self._set_attr("max", value)

    # divisions
    @property
    def divisions(self) -> Optional[int]:
        return self._get_attr("divisions")

    @divisions.setter
    def divisions(self, value: Optional[int]):
        self._set_attr("divisions", value)

    # round
    @property
    def round(self) -> Optional[int]:
        return self._get_attr("round", data_type="int", def_value=0)

    @round.setter
    def round(self, value: Optional[int]):
        self._set_attr("round", value)

    # overlay_color
    @property
    def overlay_color(self) -> Union[None, str, Dict[ControlState, str]]:
        return self.__overlay_color

    @overlay_color.setter
    def overlay_color(self, value: Union[None, str, Dict[ControlState, str]]):
        self.__overlay_color = value

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
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

    # inactive_color
    @property
    def inactive_color(self) -> Optional[str]:
        return self._get_attr("inactiveColor")

    @inactive_color.setter
    def inactive_color(self, value: Optional[str]):
        self._set_attr("inactiveColor", value)

    # thumb_color
    @property
    def thumb_color(self) -> Optional[str]:
        return self._get_attr("thumbColor")

    @thumb_color.setter
    def thumb_color(self, value: Optional[str]):
        self._set_attr("thumbColor", value)

    # on_change
    @property
    def on_change(self) -> OptionalEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalEventCallable):
        self._add_event_handler("change", handler)

    # on_change_start
    @property
    def on_change_start(self) -> OptionalEventCallable:
        return self._get_event_handler("change_start")

    @on_change_start.setter
    def on_change_start(self, handler: OptionalEventCallable):
        self._add_event_handler("change_start", handler)

    # on_change_end
    @property
    def on_change_end(self) -> OptionalEventCallable:
        return self._get_event_handler("change_end")

    @on_change_end.setter
    def on_change_end(self, handler: OptionalEventCallable):
        self._add_event_handler("change_end", handler)

    # on_focus
    @property
    def on_focus(self) -> OptionalEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalEventCallable):
        self._add_event_handler("blur", handler)
