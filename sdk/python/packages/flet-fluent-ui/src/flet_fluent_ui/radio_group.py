from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["RadioButton", "RadioGroup"]


@ft.control("FluentRadioButton")
class RadioButton(ft.Control):
    """
    One option in a :class:`~flet_fluent_ui.RadioGroup`.
    """

    value: str
    """
    The value the group takes when this option is selected.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown next to the radio button. Clicking it selects the option.
    """


@ft.control("FluentRadioGroup")
class RadioGroup(ft.LayoutControl):
    """
    A Fluent radio group: a set of options where only one can be selected.

    Example:
    ```python
    fluent.RadioGroup(
        value="medium",
        items=[
            fluent.RadioButton(value="small", label="Small"),
            fluent.RadioButton(value="medium", label="Medium"),
            fluent.RadioButton(value="large", label="Large"),
        ],
    )
    ```
    """

    items: list[RadioButton] = field(default_factory=list)
    """
    The options of this group.
    """

    value: Optional[str] = None
    """
    The :attr:`~flet_fluent_ui.RadioButton.value` of the selected option.

    If `None`, no option is selected.
    """

    horizontal: bool = False
    """
    Whether to lay out :attr:`items` in a row instead of a column.
    """

    spacing: ft.Number = 8
    """
    The space between :attr:`items`.
    """

    on_change: Optional[ft.ControlEventHandler["RadioGroup"]] = None
    """
    Called when the selected option changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`value`.
    """
