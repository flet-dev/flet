from typing import Optional

import flet as ft

__all__ = ["NumberBox"]


@ft.control("FluentNumberBox")
class NumberBox(ft.LayoutControl):
    """
    A Fluent number box: a text box for numbers, with buttons to step the
    value up and down.

    The value is checked when the user presses `Enter`, clicks outside the box
    or uses the buttons: text that is not a number is reverted, and values out
    of :attr:`min`..:attr:`max` are clamped.

    Example:
    ```python
    fluent.NumberBox(value=3, min=0, max=10)
    fluent.NumberBox(value=2.5, small_change=0.5, precision=1)
    ```
    """

    value: Optional[ft.Number] = None
    """
    The current number.

    If `None`, the box is empty.
    """

    min: Optional[ft.Number] = None
    """
    The smallest allowed value.

    If `None`, there is no lower limit.
    """

    max: Optional[ft.Number] = None
    """
    The largest allowed value.

    If `None`, there is no upper limit.
    """

    small_change: ft.Number = 1
    """
    How much the spin buttons and the `Up`/`Down` keys change the value.
    """

    large_change: ft.Number = 10
    """
    How much the `Page Up`/`Page Down` keys change the value.
    """

    precision: Optional[int] = None
    """
    The maximum number of decimal places shown. Trailing zeros are not shown.

    If `None`, up to 2 decimal places are shown. It can't be changed after the
    number box is first shown.
    """

    allow_expressions: bool = False
    """
    Whether the user can type a math expression, such as `2 + 3 * 4`, which is
    replaced with its result.
    """

    spin_buttons: bool = True
    """
    Whether the up and down buttons are shown at the end of the box.
    """

    clear_button: bool = True
    """
    Whether a button to clear the box is shown while it has focus and text.
    """

    placeholder: Optional[str] = None
    """
    The hint shown while the box is empty.
    """

    prefix: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before the number.
    """

    autofocus: bool = False
    """
    Whether this number box should be focused on initial display.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below the box, which also gets a red underline.

    Set it to tell the user that the value is not valid, and set it to `None`
    to hide it.
    """

    on_change: Optional[ft.ControlEventHandler["NumberBox"]] = None
    """
    Called when :attr:`value` changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value, or `None` when the box was cleared.
    """
