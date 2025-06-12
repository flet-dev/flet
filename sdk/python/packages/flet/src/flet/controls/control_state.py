from enum import Enum
from typing import TypeVar, Union

__all__ = ["ControlState", "ControlStateValue"]


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
ControlStateValue = Union[T, dict[ControlState, T]]
