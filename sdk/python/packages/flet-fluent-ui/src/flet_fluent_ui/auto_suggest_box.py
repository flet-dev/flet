from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["AutoSuggestBox", "AutoSuggestBoxItem"]


@ft.control("FluentAutoSuggestBoxItem")
class AutoSuggestBoxItem(ft.Control):
    """
    One suggestion in an :class:`~flet_fluent_ui.AutoSuggestBox`.
    """

    value: str
    """
    The value reported when this suggestion is chosen.
    """

    label: Optional[str] = None
    """
    The text this suggestion is matched against and shown with. It is put in
    the box when the suggestion is chosen.

    If `None`, :attr:`value` is used.
    """

    content: Optional[ft.Control] = None
    """
    A custom control shown in the list instead of :attr:`label`.
    """


@ft.control("FluentAutoSuggestBox")
class AutoSuggestBox(ft.LayoutControl):
    """
    A Fluent auto-suggest box: a text box that lists matching suggestions as
    the user types.

    Suggestions whose label contains the typed text, ignoring case, are shown.

    Example:
    ```python
    fluent.AutoSuggestBox(
        placeholder="Search fruit",
        items=[
            fluent.AutoSuggestBoxItem(value="apple", label="Apple"),
            fluent.AutoSuggestBoxItem(value="banana", label="Banana"),
            fluent.AutoSuggestBoxItem(value="cherry", label="Cherry"),
        ],
    )
    ```
    """

    items: list[AutoSuggestBoxItem] = field(default_factory=list)
    """
    The suggestions.
    """

    value: str = ""
    """
    The text in the box.
    """

    placeholder: Optional[str] = None
    """
    The hint shown while the box is empty.
    """

    prefix: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before the text.
    """

    clear_button: bool = True
    """
    Whether a button to clear the box is shown while it has focus and text.
    """

    max_popup_height: ft.Number = 380
    """
    The maximum height of the list of suggestions.
    """

    autofocus: bool = False
    """
    Whether this box should be focused on initial display.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below the box, which also gets a red underline.

    Set it to tell the user that the value is not valid, and set it to `None`
    to hide it.
    """

    on_change: Optional[ft.ControlEventHandler["AutoSuggestBox"]] = None
    """
    Called when the text changes, by typing, choosing a suggestion or
    clearing.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new text.
    """

    on_select: Optional[ft.ControlEventHandler["AutoSuggestBox"]] = None
    """
    Called when the user chooses a suggestion.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the :attr:`~flet_fluent_ui.AutoSuggestBoxItem.value` of the
    chosen suggestion.
    """
