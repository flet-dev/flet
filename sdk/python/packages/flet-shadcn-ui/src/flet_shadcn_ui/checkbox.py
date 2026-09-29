from typing import Optional

import flet as ft

__all__ = ["Checkbox"]


@ft.control("ShadCheckbox")
class Checkbox(ft.LayoutControl):
    """
    A shadcn/ui checkbox.

    Example:
    ```python
    shad.Checkbox(
        label="Accept terms and conditions",
        sublabel="You agree to our Terms of Service and Privacy Policy.",
    )
    ```
    """

    value: bool = False
    """
    Whether this checkbox is checked.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown next to this checkbox.
    """

    sublabel: Optional[ft.StrOrControl] = None
    """
    Secondary text shown below :attr:`label`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The fill color when checked.

    If `None`, the primary color of the theme is used.
    """

    unchecked_color: Optional[ft.ColorValue] = None
    """
    The fill color when unchecked.
    """

    size: Optional[ft.Number] = None
    """
    The width and height of the checkbox square.

    If `None`, defaults to `16`.
    """

    on_change: Optional[ft.ControlEventHandler["Checkbox"]] = None
    """
    Called when :attr:`value` changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value.
    """
