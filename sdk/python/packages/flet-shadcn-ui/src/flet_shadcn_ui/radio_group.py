from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["Radio", "RadioGroup"]


@ft.control("ShadRadio")
class Radio(ft.Control):
    """
    One option in a :class:`~flet_shadcn_ui.RadioGroup`.
    """

    value: str
    """
    The value the group takes when this option is selected.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown next to the radio button.
    """

    sublabel: Optional[ft.StrOrControl] = None
    """
    Secondary text shown below :attr:`label`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the radio button.

    If `None`, the primary color of the theme is used.
    """


@ft.control("ShadRadioGroup")
class RadioGroup(ft.LayoutControl):
    """
    A Shadcn radio group: a set of options where only one can be selected.

    Example:
    ```python
    shad.RadioGroup(
        value="comfortable",
        items=[
            shad.Radio(value="default", label="Default"),
            shad.Radio(value="comfortable", label="Comfortable"),
            shad.Radio(value="compact", label="Compact"),
        ],
    )
    ```
    """

    items: list[Radio] = field(default_factory=list)
    """
    The options of this group.
    """

    value: Optional[str] = None
    """
    The :attr:`~flet_shadcn_ui.Radio.value` of the selected option.

    If `None`, no option is selected.
    """

    horizontal: bool = False
    """
    Whether to lay out :attr:`items` in a row instead of a column.
    """

    spacing: Optional[ft.Number] = None
    """
    The space between :attr:`items`.

    If `None`, defaults to `4`.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown above this group.

    It turns red while :attr:`error_text` is set.
    """

    description: Optional[ft.StrOrControl] = None
    """
    Helper text shown below this group.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below this group.

    Set it after validating the value, and set it back to `None` (or an empty
    string) to clear the error.
    """

    on_change: Optional[ft.ControlEventHandler["RadioGroup"]] = None
    """
    Called when the selected option changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`value`.
    """
