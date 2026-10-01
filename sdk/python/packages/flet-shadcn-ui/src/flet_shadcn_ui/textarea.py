from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V

__all__ = ["Textarea"]


@ft.control("ShadTextarea")
class Textarea(ft.LayoutControl):
    """
    A Shadcn multi-line text input.

    Its height starts at :attr:`min_height`. The user can drag the corner to
    resize it (unless :attr:`resizable` is `False`), up to :attr:`max_height`.

    Example:
    ```python
    shad.Textarea(placeholder="Type your message here.")
    ```
    """

    value: str = ""
    """
    The current text of this textarea.
    """

    placeholder: Optional[ft.StrOrControl] = None
    """
    The hint shown while :attr:`value` is empty.
    """

    min_height: Annotated[
        ft.Number,
        V.gt(0),
        V.le_field("max_height"),
    ] = 80
    """
    The initial and smallest height.

    Raises:
        ValueError: If it is not strictly greater than `0`.
        ValueError: If it is not less than or equal to :attr:`max_height`.
    """

    max_height: Annotated[
        ft.Number,
        V.ge_field("min_height"),
    ] = 500
    """
    The largest height the user can resize this textarea to.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`min_height`.
    """

    resizable: bool = True
    """
    Whether the user can drag the bottom-right corner to change the height.
    """

    read_only: bool = False
    """
    Whether the text can be selected but not changed.
    """

    max_length: Annotated[
        Optional[int],
        V.gt(0),
    ] = None
    """
    The maximum number of characters that can be entered.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    autofocus: bool = False
    """
    Whether this textarea should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["Textarea"]] = None
    """
    Called when the text changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new text.
    """

    on_focus: Optional[ft.ControlEventHandler["Textarea"]] = None
    """
    Called when this textarea receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["Textarea"]] = None
    """
    Called when this textarea loses focus.
    """

    async def focus(self):
        """
        Requests focus for this textarea.
        """
        await self._invoke_method("focus")
