from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl

__all__ = ["TransparentPointer"]


@control("TransparentPointer")
class TransparentPointer(LayoutControl):
    """
    TransparentPointer is the solution to ["How to pass through all gestures between
    two widgets in Stack"](https://stackoverflow.com/questions/65269190/pass-trough-all-
    gestures-between-two-widgets-in-stack) problem.

    For example, if there is an [`Button`][flet.]
    inside [`Container`][flet.] with
    [`GestureDetector`][flet.] then tapping on
    a button won't be "visible" to a gesture detector behind it. With
    `TransparentPointer` a tapping event doesn't stop on a button, but goes up to the
    parent, similar to event bubbling in HTML/JS.
    """

    content: Optional[Control] = None
    """
    The `Control` that should be displayed.
    """
