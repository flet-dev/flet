from typing import Optional

import flet as ft

__all__ = ["TextBox"]


@ft.control("FluentTextBox")
class TextBox(ft.LayoutControl):
    """
    A Fluent text box.

    Example:
    ```python
    fluent.TextBox(placeholder="Email", keyboard_type=ft.KeyboardType.EMAIL)
    fluent.TextBox(placeholder="Password", password=True)
    ```
    """

    value: str = ""
    """
    The current text of this text box.
    """

    placeholder: Optional[str] = None
    """
    The hint shown while :attr:`value` is empty.
    """

    password: bool = False
    """
    Whether to hide the entered text, for example for passwords.
    """

    read_only: bool = False
    """
    Whether the text can be selected but not changed.
    """

    max_length: Optional[int] = None
    """
    The maximum number of characters that can be entered.
    """

    multiline: bool = False
    """
    Whether the text can span several lines.

    A multiline text box grows with its text, from :attr:`min_lines` up to
    :attr:`max_lines`, and `Enter` inserts a new line.
    """

    min_lines: Optional[int] = None
    """
    The minimum number of lines to occupy when :attr:`multiline` is `True`.
    """

    max_lines: Optional[int] = None
    """
    The maximum number of lines to show when :attr:`multiline` is `True`.

    If `None`, the text box grows with its text without a limit.
    """

    keyboard_type: ft.KeyboardType = ft.KeyboardType.TEXT
    """
    The type of on-screen keyboard to show.
    """

    text_align: ft.TextAlign = ft.TextAlign.START
    """
    How the text is aligned horizontally.
    """

    prefix: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before the text.
    """

    suffix: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown after the text.
    """

    autofocus: bool = False
    """
    Whether this text box should be focused on initial display.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below the box, which also gets a red underline.

    Set it to tell the user that the value is not valid, and set it to `None`
    to hide it.
    """

    on_change: Optional[ft.ControlEventHandler["TextBox"]] = None
    """
    Called when the text changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new text.
    """

    on_submit: Optional[ft.ControlEventHandler["TextBox"]] = None
    """
    Called when the user submits the text, for example by pressing `Enter`.
    """

    on_focus: Optional[ft.ControlEventHandler["TextBox"]] = None
    """
    Called when this text box receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["TextBox"]] = None
    """
    Called when this text box loses focus.
    """

    async def focus(self):
        """
        Requests focus for this text box.
        """
        await self._invoke_method("focus")
