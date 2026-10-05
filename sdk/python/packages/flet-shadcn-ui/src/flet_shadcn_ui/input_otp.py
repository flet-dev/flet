from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V, ValidationRules

__all__ = ["InputOTP"]


@ft.control("ShadInputOTP")
class InputOTP(ft.LayoutControl):
    """
    A Shadcn one-time password input: a row of single-character boxes.

    Example:
    ```python
    shad.InputOTP(length=6, groups=[3, 3])
    ```
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: ctrl.groups is None or sum(ctrl.groups) == ctrl.length,
            message="groups must add up to length",
        ),
    )

    value: str = ""
    """
    The characters entered so far.
    """

    length: Annotated[
        int,
        V.gt(0),
    ] = 6
    """
    The number of characters.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    groups: Optional[list[int]] = None
    """
    How the boxes are split into groups, as a list of group sizes that add up
    to :attr:`length`. For example, `[3, 3]` shows two groups of three.

    If `None`, all boxes form one group.

    Raises:
        ValueError: If its sizes do not add up to :attr:`length`.
    """

    separator: Optional[ft.IconDataOrControl] = None
    """
    The icon or control shown between :attr:`groups`.

    If `None`, a dot is shown.
    """

    keyboard_type: ft.KeyboardType = ft.KeyboardType.NUMBER
    """
    The type of on-screen keyboard to show.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown above this input.

    It turns red while :attr:`error_text` is set.
    """

    description: Optional[ft.StrOrControl] = None
    """
    Helper text shown below this input.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below this input. The slot borders turn red too.

    Set it after validating the value, and set it back to `None` (or an empty
    string) to clear the error.
    """

    on_change: Optional[ft.ControlEventHandler["InputOTP"]] = None
    """
    Called when the characters change.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`value`.
    """

    on_complete: Optional[ft.ControlEventHandler["InputOTP"]] = None
    """
    Called when every box is filled.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the full :attr:`value`.
    """
