from dataclasses import field

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import CrossAxisAlignment, MainAxisAlignment, Number

__all__ = ["Row"]


@control("Row")
class Row(LayoutControl, ScrollableControl, AdaptiveControl):
    """
    Displays its children in a horizontal array.

    To cause a child control to expand and fill the available horizontal space, set
    its [`expand`][(c).] property.

    Example:
    ```python
    (
        ft.Row(
            controls=[
                ft.Card(
                    shape=ft.ContinuousRectangleBorder(radius=10),
                    content=ft.Container(
                        padding=5,
                        border_radius=ft.BorderRadius.all(5),
                        bgcolor=ft.Colors.AMBER_100,
                        content=ft.Text(f"Control {i}"),
                    ),
                )
                for i in range(1, 6)
            ],
        ),
    )
    ```

    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    Defines how the child [`controls`][(c).] should be placed horizontally.
    """

    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    """
    Defines how the child [`controls`][(c).] should be placed vertically.

    Note:
        When [`wrap`][(c).] is `True`, this property doesn't support
        [`CrossAxisAlignment.STRETCH`][flet.] or
        [`CrossAxisAlignment.BASELINE`][flet.]. If either is used,
        [`CrossAxisAlignment.CENTER`][flet.] will be applied instead.
    """

    spacing: Number = 10
    """
    The spacing between the child [`controls`][(c).].

    Note:
        Has effect only when [`alignment`][(c).] is set to
        [`MainAxisAlignment.START`][flet.], [`MainAxisAlignment.END`][flet.],
        or [`MainAxisAlignment.CENTER`][flet.].
    """

    tight: bool = False
    """
    Whether this row should occupy all available horizontal space (`True`),
    or only as much as needed by its children [`controls`][(c).] (`False`).

    Note:
        Has effect only when [`wrap`][(c).] is `False`.
    """

    wrap: bool = False
    """
    Whether this row should put child [`controls`][(c).] into additional rows (runs) if
    they don't fit in a single row.
    """

    run_spacing: Number = 10
    """
    The spacing between runs when [`wrap`][(c).] is `True`.
    """

    run_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the runs should be placed in the cross-axis when [`wrap`][(c).] is `True`.
    """

    intrinsic_height: bool = False
    """
    Whether this row should be as tall as the tallest child control in
    [`controls`][(c).].
    """

    def init(self):
        super().init()
        self._internals["host_expanded"] = True
