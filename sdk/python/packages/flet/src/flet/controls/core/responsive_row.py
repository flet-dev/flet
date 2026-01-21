from dataclasses import field
from typing import Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    Number,
    ResponsiveNumber,
    ResponsiveRowBreakpoint,
)

__all__ = ["ResponsiveNumber", "ResponsiveRow", "ResponsiveRowBreakpoint"]


@control("ResponsiveRow")
class ResponsiveRow(LayoutControl, AdaptiveControl):
    """
    Allows aligning child controls to virtual columns.

    By default, a virtual grid has 12 columns, but that can be customized with
    [`columns`][(c).] property.

    Similar to `expand` property, every control has [`col`][flet.Control.]
    property which allows specifying how many columns a control should span.

    Example:
    ```python
    ft.ResponsiveRow(
        controls=[
            ft.Button(
                f"Button {i}",
                color=ft.Colors.BLUE_GREY_300,
                col={
                    ft.ResponsiveRowBreakpoint.XS: 12,
                    ft.ResponsiveRowBreakpoint.MD: 6,
                    ft.ResponsiveRowBreakpoint.LG: 3,
                },
            )
            for i in range(1, 6)
        ],
    )
    ```

    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display.
    """

    columns: ResponsiveNumber = 12
    """
    The number of virtual columns to layout children.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    Defines how the child [`controls`][(c).] should be
    placed horizontally.
    """

    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    """
    Defines how the child [`controls`][(c).] should be placed vertically.
    """

    spacing: ResponsiveNumber = 10
    """
    The spacing between controls in a row in virtual pixels.

    Note:
        Has effect only when [`alignment`][(c).] is set to
        [`MainAxisAlignment.START`][flet.], [`MainAxisAlignment.END`][flet.],
        or [`MainAxisAlignment.CENTER`][flet.].
    """

    run_spacing: ResponsiveNumber = 10
    """
    The spacing between runs.
    """

    breakpoints: dict[Union[ResponsiveRowBreakpoint, str], Number] = field(
        default_factory=lambda: {
            ResponsiveRowBreakpoint.XS: 0,
            ResponsiveRowBreakpoint.SM: 576,
            ResponsiveRowBreakpoint.MD: 768,
            ResponsiveRowBreakpoint.LG: 992,
            ResponsiveRowBreakpoint.XL: 1200,
            ResponsiveRowBreakpoint.XXL: 1400,
        }
    )
    """
    Defines the minimum widths (in px) for each breakpoint key used by responsive
    properties such as [`col`][flet.Control.], [`spacing`][flet.ResponsiveRow.],
    and [`run_spacing`][flet.ResponsiveRow.].

    Keys can be [`ResponsiveRowBreakpoint`][flet.] values or custom strings.
    Breakpoint names in responsive values must match the names used here.

    The default mirrors Bootstrap breakpoints.
    """
