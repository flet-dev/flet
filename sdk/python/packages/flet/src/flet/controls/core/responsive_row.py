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

    Online docs: https://flet.dev/docs/controls/responsiverow
    """

    controls: list[Control] = field(default_factory=list)
    columns: ResponsiveNumber = 12
    alignment: MainAxisAlignment = MainAxisAlignment.START
    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    spacing: ResponsiveNumber = 10
    run_spacing: ResponsiveNumber = 10
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

    def clean(self):
        super().clean()
        self.controls.clear()
