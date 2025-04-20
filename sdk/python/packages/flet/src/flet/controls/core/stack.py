from dataclasses import field
from enum import Enum
from typing import List, Optional

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

    This control is useful if you want to overlap several children in a simple way, for example having some text and an image, overlaid with a gradient and a button attached to the bottom.

    Stack is also useful if you want to implement implicit animations (https://flet.dev/docs/guides/python/animations/) that require knowing absolute position of a target value.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        st = ft.Stack(
            controls=[
                ft.Image(
                    src=f"https://picsum.photos/300/300",
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Image title",
                            color="white",
                            size=40,
                            weight="bold",
                            opacity=0.5,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            width=300,
            height=300,
        )

        page.add(st)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/stack
    """

    controls: List[Control] = field(default_factory=list)
    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    alignment: Optional[Alignment] = None
    fit: StackFit = StackFit.LOOSE
