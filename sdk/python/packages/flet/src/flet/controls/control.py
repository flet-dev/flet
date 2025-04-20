from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional, Union

from flet.controls.base_control import BaseControl
from flet.controls.material.badge import BadgeValue
from flet.controls.material.tooltip import TooltipValue
from flet.controls.types import Number, ResponsiveNumber

__all__ = [
    "Control",
    "OptionalControl",
]


@dataclass(kw_only=True)
class Control(BaseControl):
    expand: Optional[Union[bool, int]] = None
    expand_loose: Optional[bool] = None
    col: ResponsiveNumber = 12
    opacity: Number = 1.0
    tooltip: Optional[TooltipValue] = None
    badge: Optional[BadgeValue] = None
    visible: bool = True
    disabled: bool = False
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
