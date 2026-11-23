from typing import Optional

import flet as ft

__all__ = ["Checkbox", "ToggleButton", "ToggleSwitch"]


@ft.control("FluentToggleButton")
class ToggleButton(ft.LayoutControl):
    """
    A Fluent button that can be switched on and off, filled with the accent
    color while :attr:`checked`.

    Example:
    ```python
    fluent.ToggleButton("Bold", on_change=lambda e: print(e.data))
    fluent.ToggleButton("Italic", checked=True)
    ```
    """

    content: Optional[ft.StrOrControl] = None
    """
    The button's label.

    If a string is provided, it is wrapped in a :class:`~flet.Text` control.
    """

    checked: bool = False
    """
    Whether this button is on.
    """

    autofocus: bool = False
    """
    Whether this button should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["ToggleButton"]] = None
    """
    Called when :attr:`checked` changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value.
    """


@ft.control("FluentCheckbox")
class Checkbox(ft.LayoutControl):
    """
    A Fluent checkbox.

    Example:
    ```python
    fluent.Checkbox(label="Remember me", value=True)
    fluent.Checkbox(label="Select all", tristate=True)  # indeterminate
    fluent.Checkbox(label="Disabled", disabled=True)
    ```
    """

    value: Optional[bool] = None
    """
    Whether this checkbox is checked.

    `None` shows the indeterminate state when :attr:`tristate` is `True`, and
    unchecked otherwise.
    """

    tristate: bool = False
    """
    Whether clicking cycles through checked, indeterminate (`None`) and
    unchecked, instead of only checked and unchecked.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown next to this checkbox. Clicking it toggles the checkbox.
    """

    autofocus: bool = False
    """
    Whether this checkbox should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["Checkbox"]] = None
    """
    Called when :attr:`value` changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value.
    """


@ft.control("FluentToggleSwitch")
class ToggleSwitch(ft.LayoutControl):
    """
    A Fluent toggle switch, for turning an option on or off with an immediate
    effect.

    Example:
    ```python
    fluent.ToggleSwitch(label="Wi-Fi", value=True)
    fluent.ToggleSwitch(label="Bluetooth")
    ```
    """

    value: bool = False
    """
    Whether this switch is on.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown next to this switch. Clicking it toggles the switch.
    """

    label_first: bool = False
    """
    Whether :attr:`label` is shown before the switch instead of after it.
    """

    autofocus: bool = False
    """
    Whether this switch should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["ToggleSwitch"]] = None
    """
    Called when :attr:`value` changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value.
    """
