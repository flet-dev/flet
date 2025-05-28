from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.base_control import BaseControl
from flet.controls.material.badge import BadgeValue
from flet.controls.material.tooltip import TooltipValue
from flet.controls.types import Number, ResponsiveNumber

__all__ = [
    "Control",
    "OptionalControl"
]


@dataclass(kw_only=True)
class Control(BaseControl):
    expand: Optional[Union[bool, int]] = None
    expand_loose: Optional[bool] = None
    col: ResponsiveNumber = 12  # todo: if dict, validate keys with those in parent (ResponsiveRow.breakpoints)
    opacity: Number = 1.0
    """
    Defines the transparency of the control.
    It's ranges from `0.0` (completely transparent) to 
    `1.0` (completely opaque without any transparency).
    
    Defaults to `1.0´.
    """
    tooltip: Optional[TooltipValue] = None
    """
    A tooltip message to show when the user hovers over the control.
    
    The tooltip can be of type `str` or `Tooltip`.
    """

    badge: Optional[BadgeValue] = None
    """
    A badge to show on top of the control.
    
    The badge can be of type `str` or `Badge`.
    """

    visible: bool = True
    """
    Whether the control is visible or not. 

    Defaults to `True`.
    """

    disabled: bool = False
    """
    Whether the control is disabled or not. 
    
    Defaults to `False`.
    """

    rtl: bool = False

    def before_update(self):
        super().before_update()
        assert (
            0.0 <= self.opacity <= 1.0
        ), "opacity must be between 0.0 and 1.0 inclusive"
        assert self.expand is None or isinstance(
            self.expand, (bool, int)
        ), "expand must be of bool or int type"

    def clean(self) -> None:
        raise Exception("Deprecated!")


# Typing
OptionalControl = Optional[Control]
