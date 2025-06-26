from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.types import ClipBehavior

__all__ = ["Stack", "StackFit"]


class StackFit(Enum):
    LOOSE = "loose"
    EXPAND = "expand"
    PASS_THROUGH = "passThrough"


@control("Stack")
class Stack(ConstrainedControl, AdaptiveControl):
    """
    A control that positions its children on top of each other.

    This control is useful if you want to overlap several children in a simple way,
    for example having some text and an image, overlaid with a gradient and a button
    attached to the bottom.

    Stack is also useful if you want to implement implicit animations
    (https://flet.dev/docs/guides/python/animations/) that require knowing absolute
    position of a target value.

    Online docs: https://flet.dev/docs/controls/stack
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display inside the Stack. The last control in the list is
    displayed on top.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior)
    and defaults to `ClipBehavior.HARD_EDGE`.
    """

    alignment: Optional[Alignment] = None
    """
    The alignment of the non-positioned (those that do not specify an alignment - ex
    neither top nor bottom - in a particular axis and partially-positioned `controls`.
    """

    fit: StackFit = StackFit.LOOSE
    """
    How to size the non-positioned `controls`.

    Value is of type [`StackFit`](https://flet.dev/docs/reference/types/stackfit) and
    defaults to `StackFit.LOOSE`.
    """
