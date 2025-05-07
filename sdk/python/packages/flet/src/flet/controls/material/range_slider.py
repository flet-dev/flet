from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["RangeSlider"]


@control("RangeSlider")
class RangeSlider(ConstrainedControl):
    """
    A Material Design range slider. Used to select a range from a range of values.
    A range slider can be used to select from either a continuous or a discrete
    set of values.
    The default is to use a continuous range of values from min to max.

    Example:
        ```
    import flet as ft


    def range_slider_changed(e):
        print(f"On change! Values are ({e.control.start_value}, "
        f"{e.control.end_value})")


    def range_slider_started_change(e):
        print(
            f"On change start! Values are ({e.control.start_value}, "
            f"{e.control.end_value})"
        )


    def range_slider_ended_change(e):
        print(f"On change end! Values are ({e.control.start_value}, "
        f"{e.control.end_value})")


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

    start_value: Number
    end_value: Number
    label: Optional[str] = None
    min: OptionalNumber = None
    max: OptionalNumber = None
    divisions: Optional[int] = None
    round: Optional[int] = None
    active_color: OptionalColorValue = None
    inactive_color: OptionalColorValue = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    on_change: OptionalControlEventCallable = None
    on_change_start: OptionalControlEventCallable = None
    on_change_end: OptionalControlEventCallable = None

    def before_update(self):
        # if value is not None:
        #     if self.max is not None:
        #         assert value <= self.max, "min must be less than or equal to max"
        #
        # if value is not None:
        #     if self.min is not None:
        #         assert value >= self.min, "max must be greater than or equal to min"
        pass
