from dataclasses import field
from typing import Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    Number,
    ResponsiveNumber,
    ResponsiveRowBreakpoint,
)
from flet.utils.validation import V, ValidationRules

__all__ = ["ResponsiveNumber", "ResponsiveRow", "ResponsiveRowBreakpoint"]


@control("ResponsiveRow")
class ResponsiveRow(LayoutControl, ScrollableControl, AdaptiveControl):
    """
    Allows aligning child controls to virtual columns.

    By default, a virtual grid has 12 columns, but that can be customized with
    :attr:`columns` property.

    Similar to `expand` property, every control has :attr:`~flet.Control.col`
    property which allows specifying how many columns a control should span.

    Use :attr:`~flet.ScrollableControl.scroll` to enable vertical scrolling when
    the responsive content is taller than the available height.

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

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: (
                ctrl.columns > 0
                if isinstance(ctrl.columns, (int, float))
                else all(v > 0 for v in ctrl.columns.values())
            ),
            message="columns must be greater than 0 for all breakpoints",
        ),
    )

    columns: ResponsiveNumber = 12
    """
    The number of virtual columns to layout children.

    Raises:
        ValueError: If it is not strictly greater than `0`.
        ValueError: If any breakpoint-specific value is not strictly greater than `0`.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    Defines how the child :attr:`controls` should be placed horizontally.
    """

    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    """
    Defines how the child :attr:`controls` should be placed vertically.
    """

    spacing: ResponsiveNumber = 10
    """
    The spacing between controls in a row in virtual pixels.

    Note:
        Has effect only when :attr:`alignment` is set to
        :attr:`flet.MainAxisAlignment.START`, :attr:`flet.MainAxisAlignment.END`,
        or :attr:`flet.MainAxisAlignment.CENTER`.
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
    Defines the minimum widths (in px) for each breakpoint key used by responsive \
    properties such as :attr:`~flet.Control.col`, :attr:`~flet.ResponsiveRow.spacing`, \
    and :attr:`~flet.ResponsiveRow.run_spacing`.

    Keys can be :class:`~flet.ResponsiveRowBreakpoint` values or custom strings.
    Breakpoint names in responsive values must match the names used here.

    The default mirrors Bootstrap breakpoints.
    """
