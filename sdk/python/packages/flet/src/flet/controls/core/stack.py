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
    LOOSE = "loose"
    EXPAND = "expand"
    PASS_THROUGH = "passThrough"


@control("Stack")
class Stack(LayoutControl, AdaptiveControl):
    """
    Positions its children on top of each other, following a LIFO (Last In First Out)
    order.

    This control is useful if you want to overlap several children in a simple way.
    For example having some text and an image, overlaid with a gradient and a button
    attached to the bottom.

    Stack is also useful if you want to implement implicit animations
    (https://flet.dev/docs/guides/python/animations/) that require knowing absolute
    position of a target value.

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
    Specifies the alignment for non-positioned (those without explicit
    alignment properties such as [`top`][flet.LayoutControl.]
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
