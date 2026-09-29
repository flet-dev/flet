from typing import Optional

import flet as ft

__all__ = ["Input"]


@ft.control("ShadInput")
class Input(ft.LayoutControl):
    """
    A shadcn/ui text input.

    Example:
    ```python
    shad.Input(placeholder="Email", keyboard_type=ft.KeyboardType.EMAIL)
    shad.Input(placeholder="Password", password=True)
    ```
    """

    value: str = ""
    """
    The current text of this input.
    """

    placeholder: Optional[ft.StrOrControl] = None
    """
    The hint shown while :attr:`value` is empty.
    """

    password: bool = False
    """
    Whether to hide the entered text, for example for passwords.
    """

    obscuring_character: str = "•"
    """
    The character used to hide the entered text when :attr:`password` is `True`.
    """

    read_only: bool = False
    """
    Whether the text can be selected but not changed.
    """

    max_length: Optional[int] = None
    """
    The maximum number of characters that can be entered.
    """

    min_lines: Optional[int] = None
    """
    The minimum number of lines to occupy.
    """

    max_lines: Optional[int] = 1
    """
    The maximum number of lines to show.

    If `None`, the input grows with its text.
    """

    keyboard_type: ft.KeyboardType = ft.KeyboardType.TEXT
    """
    The type of on-screen keyboard to show.
    """

    text_align: ft.TextAlign = ft.TextAlign.START
    """
    How the text is aligned horizontally.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before the text.
    """

    trailing: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown after the text.
    """

    autofocus: bool = False
    """
    Whether this input should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["Input"]] = None
    """
    Called when the text changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new text.
    """

    on_submit: Optional[ft.ControlEventHandler["Input"]] = None
    """
    Called when the user submits the text, for example by pressing `Enter`.
    """

    on_click: Optional[ft.ControlEventHandler["Input"]] = None
    """
    Called when this input is clicked.
    """

    on_focus: Optional[ft.ControlEventHandler["Input"]] = None
    """
    Called when this input receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["Input"]] = None
    """
    Called when this input loses focus.
    """

    async def focus(self):
        """
        Requests focus for this input.
        """
        await self._invoke_method("focus")
