from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import OptionalColorValue, OptionalNumber

__all__ = ["ProgressBar"]


@control("ProgressBar")
class ProgressBar(ConstrainedControl):
    """
    A material design linear progress indicator, also known as a progress bar.

    A control that shows progress along a line.

    Example:

    ```
    from time import sleep

    import flet as ft

    def main(page: ft.Page):
        pb = ft.ProgressBar(width=400)

        page.add(
            ft.Text("Linear progress indicator", style="headlineSmall"),
            ft.Column([ ft.Text("Doing something..."), pb]),
            ft.Text("Indeterminate progress bar", style="headlineSmall"),
            ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
        )

        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)
            page.update()

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/progressbar
    """

    value: OptionalNumber = None
    bar_height: OptionalNumber = 4.0
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    border_radius: OptionalBorderRadiusValue = None
    semantics_label: Optional[str] = None
    semantics_value: OptionalNumber = None
    stop_indicator_color: OptionalColorValue = None
    stop_indicator_radius: OptionalNumber = None
    track_gap: OptionalNumber = None
    year_2023: Optional[bool] = None

    def before_update(self):
        super().before_update()
        assert self.value is None or self.value >= 0, "value cannot be negative"
        assert (
            self.bar_height is None or self.bar_height >= 0
        ), "bar_height cannot be negative"
        assert (
            self.semantics_value is None or self.semantics_value >= 0
        ), "semantics_value cannot be negative"
