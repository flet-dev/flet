from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["ComboBox", "ComboBoxItem", "EditableComboBox"]


@ft.control("FluentComboBoxItem")
class ComboBoxItem(ft.Control):
    """
    One option in a :class:`~flet_fluent_ui.ComboBox` or an
    :class:`~flet_fluent_ui.EditableComboBox`.
    """

    value: str
    """
    The value the combo box takes when this option is chosen.
    """

    text: Optional[str] = None
    """
    The text of this option, shown in the list and in the closed combo box.

    If `None`, :attr:`value` is shown.
    """

    content: Optional[ft.Control] = None
    """
    A custom control shown instead of :attr:`text`.
    """


@ft.control("FluentComboBox")
class ComboBox(ft.LayoutControl):
    """
    A Fluent combo box: a button that opens a list of options to pick one from.

    Example:
    ```python
    fluent.ComboBox(
        placeholder="Pick a color",
        items=[
            fluent.ComboBoxItem(value="red", text="Red"),
            fluent.ComboBoxItem(value="green", text="Green"),
            fluent.ComboBoxItem(value="blue", text="Blue"),
        ],
    )
    ```
    """

    items: list[ComboBoxItem] = field(default_factory=list)
    """
    The options to choose from.
    """

    value: Optional[str] = None
    """
    The :attr:`~flet_fluent_ui.ComboBoxItem.value` of the chosen option.

    If `None`, :attr:`placeholder` is shown.
    """

    placeholder: Optional[ft.StrOrControl] = None
    """
    The hint shown while no option is chosen.
    """

    expand_to_fit: bool = False
    """
    Whether the closed combo box fills the width it is given, instead of
    fitting its widest option.
    """

    autofocus: bool = False
    """
    Whether this combo box should be focused on initial display.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below the combo box.

    Set it to tell the user that the value is not valid, and set it to `None`
    to hide it.
    """

    on_change: Optional[ft.ControlEventHandler["ComboBox"]] = None
    """
    Called when the chosen option changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`value`.
    """

    on_open: Optional[ft.ControlEventHandler["ComboBox"]] = None
    """
    Called when the list of options opens.
    """

    on_close: Optional[ft.ControlEventHandler["ComboBox"]] = None
    """
    Called when the list of options closes.
    """


@ft.control("FluentEditableComboBox")
class EditableComboBox(ft.LayoutControl):
    """
    A Fluent combo box that the user can also type into, to enter a value
    that is not one of the options.

    The box fills the width it is given: give it a `width` in a row.

    Example:
    ```python
    fluent.EditableComboBox(
        width=200,
        value="12",
        items=[fluent.ComboBoxItem(value=str(size)) for size in [8, 10, 12, 14]],
    )
    ```
    """

    items: list[ComboBoxItem] = field(default_factory=list)
    """
    The options to choose from.

    Picking an option puts its :attr:`~flet_fluent_ui.ComboBoxItem.value`
    into the box, so the values should read well.
    """

    value: str = ""
    """
    The text in the box.

    It is updated when the user picks an option, presses Enter or leaves the
    box, not on every key press.
    """

    autofocus: bool = False
    """
    Whether this combo box should be focused on initial display.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below the box.

    Set it to tell the user that the value is not valid, and set it to `None`
    to hide it.
    """

    on_change: Optional[ft.ControlEventHandler["EditableComboBox"]] = None
    """
    Called when the user picks an option or enters other text.

    :attr:`value` holds the new text.
    """

    on_focus: Optional[ft.ControlEventHandler["EditableComboBox"]] = None
    """
    Called when the box receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["EditableComboBox"]] = None
    """
    Called when the box loses focus.
    """

    async def focus(self):
        """
        Requests focus for this combo box.
        """
        await self._invoke_method("focus")
