from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["Select", "SelectOption"]


@ft.control("ShadSelectOption")
class SelectOption(ft.Control):
    """
    One option in a :class:`~flet_shadcn_ui.Select`.
    """

    value: str
    """
    The value the select takes when this option is chosen.
    """

    text: Optional[str] = None
    """
    The text of this option, shown in the list and in the closed select.

    If `None`, :attr:`value` is shown.
    """

    content: Optional[ft.Control] = None
    """
    A custom control shown instead of :attr:`text`.
    """


@ft.control("ShadSelect")
class Select(ft.LayoutControl):
    """
    A Shadcn select: a button that opens a list of options to choose one from.

    Example:
    ```python
    shad.Select(
        placeholder="Select a fruit",
        options=[
            shad.SelectOption(value="apple", text="Apple"),
            shad.SelectOption(value="banana", text="Banana"),
        ],
    )
    ```
    """

    options: list[SelectOption] = field(default_factory=list)
    """
    The options to choose from.
    """

    value: Optional[str] = None
    """
    The :attr:`~flet_shadcn_ui.SelectOption.value` of the chosen option.

    If `None`, :attr:`placeholder` is shown.
    """

    placeholder: Optional[ft.StrOrControl] = None
    """
    The content shown while no option is chosen.
    """

    allow_deselection: bool = False
    """
    Whether choosing the selected option again clears :attr:`value`.
    """

    min_width: Optional[ft.Number] = None
    """
    The smallest width of the closed select and its list of options.

    If `None`, defaults to `128`.
    """

    max_height: Optional[ft.Number] = None
    """
    The largest height of the list of options before it scrolls.

    If `None`, defaults to `384`.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown above this select.

    It turns red while :attr:`error_text` is set.
    """

    description: Optional[ft.StrOrControl] = None
    """
    Helper text shown below this select.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below this select. The border turns red too.

    Set it after validating the value, and set it back to `None` (or an empty
    string) to clear the error.
    """

    on_change: Optional[ft.ControlEventHandler["Select"]] = None
    """
    Called when the chosen option changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`value`, or `None` if it was cleared.
    """
