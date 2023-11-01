from typing import Any, Optional, Union, Tuple, List

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class RangeSlider(ConstrainedControl):
    """
    A Material Design range slider. Used to select a range from a range of values.
    A range slider can be used to select from either a continuous or a discrete set of values.
    The default is to use a continuous range of values from min to max.

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

    Online docs: https://flet.dev/docs/controls/rangeslider
    """

    def __init__(
        self,
        start_value: [float],
        end_value: [float],
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        #
        # Specific
        #
        # value: OptionalNumber = None,
        # label: Optional[str] = None,
        # labels: Union[None, Tuple[str, str], List[str]] = None,
        # start_label: Optional[str] = None,
        # end_label: Optional[str] = None,
        label: Optional[str] = None,
        min: OptionalNumber = None,
        max: OptionalNumber = None,
        divisions: Optional[int] = None,
        round: Optional[int] = None,
        # autofocus: Optional[bool] = None,
        active_color: Optional[str] = None,
        inactive_color: Optional[str] = None,
        # thumb_color: Optional[str] = None,
        on_change=None,
        on_change_start=None,
        on_change_end=None,
        on_focus=None,
        on_blur=None,
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
        self.start_value = start_value
        self.end_value = end_value
        # self.start_label = start_label
        # self.end_label = end_label
        self.label = label

        self.min = min
        self.max = max
        self.divisions = divisions
        self.round = round
        # self.autofocus = autofocus
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.on_change = on_change
        self.on_change_start = on_change_start
        self.on_change_end = on_change_end
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "rangeslider"

    def _before_build_command(self):
        super()._before_build_command()

    # start_value
    @property
    def start_value(self) -> float:
        return self._get_attr("startvalue")

    @start_value.setter
    def start_value(self, value: float):
        self._set_attr("startvalue", value)

    # end_value
    @property
    def end_value(self) -> float:
        return self._get_attr("endvalue")

    @end_value.setter
    def end_value(self, value: float):
        self._set_attr("endvalue", value)

    # label
    @property
    def label(self) -> str:
        return self._get_attr("label")

    @label.setter
    def label(self, value: str):
        self._set_attr("label", value)

    # # start_label
    # @property
    # def start_label(self) -> str:
    #     return self._get_attr("startlabel")

    # @start_label.setter
    # def start_label(self, value: str):
    #     self._set_attr("startlabel", value)

    # # end_label
    # @property
    # def end_label(self) -> str:
    #     return self._get_attr("endlabel")

    # @end_label.setter
    # def end_label(self, value: str):
    #     self._set_attr("endlabel", value)

    # min
    @property
    def min(self) -> OptionalNumber:
        return self._get_attr("min")

    @min.setter
    def min(self, value: OptionalNumber):
        self._set_attr("min", value)

    # max
    @property
    def max(self) -> OptionalNumber:
        return self._get_attr("max")

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
        return self._get_attr("round")

    @round.setter
    def round(self, value: Optional[int]):
        self._set_attr("round", value)

    # # autofocus
    # @property
    # def autofocus(self) -> Optional[bool]:
    #     return self._get_attr("autofocus", data_type="bool", def_value=False)

    # @autofocus.setter
    # def autofocus(self, value: Optional[bool]):
    #     self._set_attr("autofocus", value)

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

    # # thumb_color
    # @property
    # def thumb_color(self):
    #     return self._get_attr("thumbColor")

    # @thumb_color.setter
    # def thumb_color(self, value):
    #     self._set_attr("thumbColor", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # on_change_start
    @property
    def on_change_start(self):
        return self._get_event_handler("change_start")

    @on_change_start.setter
    def on_change_start(self, handler):
        self._add_event_handler("change_start", handler)

    # on_change_end
    @property
    def on_change_end(self):
        return self._get_event_handler("change_end")

    @on_change_end.setter
    def on_change_end(self, handler):
        self._add_event_handler("change_end", handler)

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
