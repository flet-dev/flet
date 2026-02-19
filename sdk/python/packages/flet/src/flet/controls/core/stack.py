from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ClipBehavior

__all__ = ["Stack", "StackFit"]


class StackFit(Enum):
    """
    How to size the non-positioned children of a [`Stack`][flet.].
    """

    LOOSE = "loose"
    """
    The constraints passed to the stack from its parent are loosened.

    For example, if the stack has constraints that force it to `350x600`, then
    this would allow the non-positioned children of the stack to have any
    width from zero to `350` and any height from zero to `600`.
    """

    EXPAND = "expand"
    """
    The constraints passed to the stack from its parent are tightened to the
    biggest size allowed.

    For example, if the [`Stack`][flet.] has loose constraints with a width in the range
    `10` to `100` and a height in the range `0` to `600`, then the non-positioned
    children of the stack would all be sized as `100` pixels wide and `600` high.
    """

    PASS_THROUGH = "passThrough"
    """
    The constraints passed to the stack from its parent are passed unmodified
    to the non-positioned children.

    For example, if a [`Stack`][flet.] is an expanded child of a [`Row`][flet.], the
    horizontal constraints will be tight and the vertical constraints will be loose.
    """


@control("Stack")
class Stack(LayoutControl, AdaptiveControl):
    """
    Positions its children on top of each other, following a LIFO (Last In First Out) \
    order.

    This control is useful if you want to overlap several children in a simple way.
    For example having some text and an image, overlaid with a gradient and a button
    attached to the bottom.

    Stack is also useful if you want to implement implicit animations
    (https://docs.flet.dev/cookbook/animations) that require knowing absolute
    position of a target value.

    Example:
    ```python
    ft.Stack(
            width=300,
            height=300,
            controls=[
                ft.Image(
                    src="https://picsum.photos/300/300",
                    width=300,
                    height=300,
                    fit=ft.BoxFit.CONTAIN,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value="Image title",
                            color=ft.Colors.SURFACE_TINT,
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            opacity=0.5,
                        )
                    ],
                ),
            ],
        )
    ```
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display.

    For the display order, it follows the order of the list,
    so the last control in the list will be displayed on top (LIFO - Last In First Out).
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The content will be clipped (or not) according to this option.
    """

    alignment: Optional[Alignment] = None
    """
    Specifies the alignment for non-positioned (those without explicit alignment \
    properties such as [`top`][flet.LayoutControl.]
    or [`bottom`][flet.LayoutControl.]) and
    partially-positioned [`controls`][(c).].
    """

    fit: StackFit = StackFit.LOOSE
    """
    How to size the non-positioned [`controls`][(c).].
    """

    def init(self):
        super().init()
        self._internals["host_positioned"] = True
