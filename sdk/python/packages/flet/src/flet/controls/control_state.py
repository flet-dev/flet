from enum import Enum
from typing import Dict, Optional, TypeVar, Union

__all__ = ["ControlState", "ControlStateValue", "OptionalControlStateValue"]


class ControlState(Enum):
    HOVERED = "hovered"
    FOCUSED = "focused"
    PRESSED = "pressed"
    DRAGGED = "dragged"
    SELECTED = "selected"
    SCROLLED_UNDER = "scrolledUnder"
    DISABLED = "disabled"
    ERROR = "error"
    DEFAULT = "default"


T = TypeVar("T")
ControlStateValue = Union[T, Dict[ControlState, T]]
OptionalControlStateValue = Optional[ControlStateValue]
