from typing import Optional

import flet as ft
from flet_fluent_ui.types import PasswordRevealMode

__all__ = ["PasswordBox"]


@ft.control("FluentPasswordBox")
class PasswordBox(ft.LayoutControl):
    """
    A Fluent password box: a text box that hides what is typed, with a button
    to reveal it.

    Example:
    ```python
    fluent.PasswordBox(placeholder="Password", value="secret")
    fluent.PasswordBox(
        placeholder="PIN", reveal_mode=fluent.PasswordRevealMode.HIDDEN
    )
    ```
    """

    value: str = ""
    """
    The current password.
    """

    placeholder: Optional[str] = None
    """
    The hint shown while :attr:`value` is empty.
    """

    reveal_mode: PasswordRevealMode = PasswordRevealMode.PEEK
    """
    Whether and how the user can see the password.
    """

    read_only: bool = False
    """
    Whether the password can be selected but not changed.
    """

    prefix: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before the password.
    """

    autofocus: bool = False
    """
    Whether this password box should be focused on initial display.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below the box, which also gets a red underline.

    Set it to tell the user that the value is not valid, and set it to `None`
    to hide it.
    """

    on_change: Optional[ft.ControlEventHandler["PasswordBox"]] = None
    """
    Called when the password changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new password.
    """

    on_submit: Optional[ft.ControlEventHandler["PasswordBox"]] = None
    """
    Called when the user submits the password, for example by pressing `Enter`.
    """

    on_focus: Optional[ft.ControlEventHandler["PasswordBox"]] = None
    """
    Called when this password box receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["PasswordBox"]] = None
    """
    Called when this password box loses focus.
    """

    async def focus(self):
        """
        Requests focus for this password box.
        """
        await self._invoke_method("focus")
