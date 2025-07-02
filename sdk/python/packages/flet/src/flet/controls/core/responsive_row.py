from dataclasses import field
from typing import Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    Number,
    ResponsiveNumber,
    ResponsiveRowBreakpoint,
)

__all__ = ["ResponsiveRow", "ResponsiveRowBreakpoint", "ResponsiveNumber"]


@control("ResponsiveRow")
class ResponsiveRow(ConstrainedControl, AdaptiveControl):
    """
    ResponsiveRow allows aligning child controls to virtual columns. By default, a
    virtual grid has 12 columns, but that can be customized with
    `ResponsiveRow.columns` property.

    Similar to `expand` property, every control now has `col` property which allows
    specifying how many columns a control should span.
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display inside the ResponsiveRow.
    """

    columns: ResponsiveNumber = 12
    """
    The number of virtual columns to layout children.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the child Controls should be placed horizontally.

    Value is of type
    [`MainAxisAlignment`](https://flet.dev/docs/reference/types/mainaxisalignment).
    """

    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    """
    How the child Controls should be placed vertically.

    Value is of type
    [`CrossAxisAlignment`](https://flet.dev/docs/reference/types/crossaxisalignment).
    """

    spacing: ResponsiveNumber = 10
    """
    Spacing between controls in a row in virtual pixels.

    It is applied only when `alignment` is set to `MainAxisAlignment.START`,
    `MainAxisAlignment.END` or `MainAxisAlignment.CENTER`.
    """

    run_spacing: ResponsiveNumber = 10
    """
    Spacing between runs when row content is wrapped on multiple lines.
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
    TBD
    """

    def clean(self):
        super().clean()
        self.controls.clear()
