from typing import Any, Dict, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    ControlState,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
)


class RangeSlider(ConstrainedControl):
    """
    A Material Design range slider. Used to select a range from a range of values.
    A range slider can be used to select from either a continuous or a discrete set of values.
    The default is to use a continuous range of values from min to max.

    Example:
        ```
    import flet as ft


    def range_slider_changed(e):
        print(f"On change! Values are ({e.control.start_value}, {e.control.end_value})")


    def range_slider_started_change(e):
        print(
            f"On change start! Values are ({e.control.start_value}, {e.control.end_value})"
        )


    def range_slider_ended_change(e):
        print(f"On change end! Values are ({e.control.start_value}, {e.control.end_value})")


    def main(page: ft.Page):
        range_slider = ft.RangeSlider(
            min=0,
            max=50,
            start_value=10,
            divisions=10,
            end_value=20,
            inactive_color=ft.colors.GREEN_300,
            active_color=ft.colors.GREEN_700,
            overlay_color=ft.colors.GREEN_100,
            on_change=range_slider_changed,
            on_change_start=range_slider_started_change,
            on_change_end=range_slider_ended_change,
            label="{value}%",
        )

        page.add(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Range slider", size=20, weight=ft.FontWeight.BOLD),
                    range_slider,
                ],
            )
        )


    ft.app(target=main)
        ```

        -----

    Online docs: https://flet.dev/docs/controls/rangeslider
    """

    def __init__(
        self,
        start_value: float,
        end_value: float,
        label: Optional[str] = None,
        min: OptionalNumber = None,
        max: OptionalNumber = None,
        divisions: Optional[int] = None,
        round: Optional[int] = None,
        active_color: Optional[str] = None,
        inactive_color: Optional[str] = None,
        overlay_color: Union[None, str, Dict[ControlState, str]] = None,
        on_change: OptionalEventCallable = None,
        on_change_start: OptionalEventCallable = None,
        on_change_end: OptionalEventCallable = None,
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
        on_animation_end: OptionalEventCallable = None,
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
        self.start_value = start_value
        self.end_value = end_value
        self.label = label

        self.min = min
        self.max = max
        self.divisions = divisions
        self.round = round
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.overlay_color = overlay_color
        self.on_change = on_change
        self.on_change_start = on_change_start
        self.on_change_end = on_change_end

    def _get_control_name(self):
        return "rangeslider"

    def before_update(self):
        super().before_update()
        self._set_attr_json("overlayColor", self.__overlay_color)

    # start_value
    @property
    def start_value(self) -> float:
        return self._get_attr("startValue", data_type="float")

    @start_value.setter
    def start_value(self, value: float):
        self._set_attr("startValue", value)

    # end_value
    @property
    def end_value(self) -> float:
        return self._get_attr("endValue", data_type="float")

    @end_value.setter
    def end_value(self, value: float):
        self._set_attr("endValue", value)

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # min
    @property
    def min(self) -> OptionalNumber:
        return self._get_attr("min", data_type="float")

    @min.setter
    def min(self, value: OptionalNumber):
        if value is not None:
            if self.max is not None:
                assert value <= self.max, "min must be less than or equal to max"
        self._set_attr("min", value)

    # max
    @property
    def max(self) -> OptionalNumber:
        return self._get_attr("max", data_type="float")

    @max.setter
    def max(self, value: OptionalNumber):
        if value is not None:
            if self.min is not None:
                assert value >= self.min, "max must be greater than or equal to min"
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

    # overlay_color
    @property
    def overlay_color(self) -> Union[None, str, Dict[ControlState, str]]:
        return self.__overlay_color

    @overlay_color.setter
    def overlay_color(self, value: Union[None, str, Dict[ControlState, str]]):
        self.__overlay_color = value

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
