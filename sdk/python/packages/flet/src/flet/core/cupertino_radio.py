from dataclasses import field
from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    OptionalControlEventCallable,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

__all__ = ["CupertinoRadio"]


@control("CupertinoRadio")
class CupertinoRadio(ConstrainedControl):
    """
    Radio buttons let people select a single option from two or more choices.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoradio
    """

    label: Optional[str] = None
    value: str = field(default="")
    label_position: LabelPosition = field(default=LabelPosition.RIGHT)
    fill_color: Optional[ColorValue] = None
    active_color: Optional[ColorValue] = None
    inactive_color: Optional[ColorValue] = None
    autofocus: bool = field(default=False)
    use_checkmark_style: bool = field(default=False)
    toggleable: bool = field(default=False)
    focus_color: Optional[ColorValue] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
