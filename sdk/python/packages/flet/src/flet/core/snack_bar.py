from enum import Enum
from typing import Optional

from flet.core.buttons import OutlinedBorder
from flet.core.control import Control, control
from flet.core.margin import OptionalMarginValue
from flet.core.padding import OptionalPaddingValue
from flet.core.types import (
    ClipBehavior,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["SnackBar", "SnackBarBehavior", "DismissDirection"]


class SnackBarBehavior(Enum):
    FIXED = "fixed"
    FLOATING = "floating"


class DismissDirection(Enum):
    NONE = "none"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    END_TO_START = "endToStart"
    START_TO_END = "startToEnd"
    UP = "up"
    DOWN = "down"


@control("SnackBar")
class SnackBar(Control):
    """
    A lightweight message with an optional action which briefly displays at the bottom of the screen.

    Example:
    ```
    import flet as ft

    class Data:
        def __init__(self) -> None:
            self.counter = 0

    d = Data()

    def main(page):

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Hello, world!"),
            action="Alright!",
        )
        page.snack_bar.open = True

        def on_click(e):
            page.snack_bar = ft.SnackBar(ft.Text(f"Hello {d.counter}"))
            page.snack_bar.open = True
            d.counter += 1
            page.update()

        page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/snackbar
    """

    content: Control
    open: bool = False
    behavior: Optional[SnackBarBehavior] = None
    dismiss_direction: Optional[DismissDirection] = None
    show_close_icon: bool = False
    action: Optional[str] = None
    action_color: OptionalColorValue = None
    close_icon_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    duration: Optional[int] = None
    margin: OptionalMarginValue = None
    padding: OptionalPaddingValue = None
    width: OptionalNumber = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    clip_behavior: Optional[ClipBehavior] = None
    action_overflow_threshold: Number = 0.25
    on_action: OptionalControlEventCallable = None
    on_visible: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.action_overflow_threshold is None
            or 0 <= self.action_overflow_threshold <= 1
        ), "action_overflow_threshold must be between 0 and 1 inclusive"
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
