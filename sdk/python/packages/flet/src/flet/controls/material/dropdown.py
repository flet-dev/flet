from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.material.form_field_control import InputBorder
from flet.controls.material.icons import Icons
from flet.controls.material.textfield import InputFilter, TextCapitalization
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
    TextAlign,
)

__all__ = ["Dropdown", "DropdownOption"]


@control("DropdownOption")
class DropdownOption(Control):
    """
    Represents an item in a dropdown. Either `key` or `text` must be specified, else an
    `AssertionError` will be raised.
    """

    key: Optional[str] = None
    """
    Option's key. If not specified [`text`][flet.DropdownOption.text] will
    be used as fallback.
    """

    text: Optional[str] = None
    """
    Option's display text. If not specified `key` will be used as fallback.
    """

    content: Optional[Control] = None
    """
    A `Control` to display in this option. If not specified, `text` will be used as
    fallback, else `text` will be ignored.
    """

    leading_icon: Optional[IconDataOrControl] = None
    """
    An optional icon to display before the content or text.
    """

    trailing_icon: Optional[IconDataOrControl] = None
    """
    An optional icon to display after the content or text.
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this menu item's appearance.
    """

    def before_update(self):
        super().before_update()
        assert self.key is not None or self.text is not None, (
            "key or text must be specified"
        )


Option = DropdownOption


@control("Dropdown")
class Dropdown(ConstrainedControl):
    """
    A dropdown control that allows users to select a single option from a list of
    options.
    """

    value: Optional[str] = None
    """
    [`key`][flet.DropdownOption.key] value of the selected option.
    """

    options: list[DropdownOption] = field(default_factory=list)
    """
    A list of options to display in the dropdown.
    """

    autofocus: bool = False
    """
    Whether the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    text_align: TextAlign = TextAlign.START
    """
    The text align for the TextField of the Dropdown.
    """

    elevation: Optional[ControlStateValue[Optional[Number]]] = 8
    """
    The dropdown's menu elevation in various [`ControlState`][flet.ControlState]
    states.
    """

    enable_filter: bool = False
    """
    Determine if the menu list can be filtered by the text input. Defaults to false.

    If set to true, dropdown menu will show a filtered list. The filtered list will
    contain items that match the text provided by the input field, with a
    case-insensitive comparison.
    """

    enable_search: bool = True
    """
    Determine if the first item that matches the text input can be highlighted.
    """

    editable: bool = False
    """
    TBD
    """

    menu_height: Optional[Number] = None
    """
    The height of the dropdown menu.

    If this is `None`, the menu will display as many
    items as possible on the screen.
    """

    menu_width: Optional[Number] = None
    """
    The width of the dropdown menu.

    If this is `None`, the menu width will be the same as
    input textfield width.
    """

    expanded_insets: Optional[PaddingValue] = None
    """
    TBD
    """

    selected_suffix: Optional[Control] = None
    """
    TBD
    """

    input_filter: Optional[InputFilter] = None
    """
    TBD
    """

    capitalization: Optional[TextCapitalization] = None
    """
    TBD
    """

    trailing_icon: IconDataOrControl = Icons.ARROW_DROP_DOWN
    """
    An icon to display at the end of the text field.
    """

    leading_icon: Optional[IconDataOrControl] = None
    """
    An optional Icon at the front of the text input field inside the decoration box.

    If this is not null, the menu items will have extra paddings to
    be aligned with the text in the text field.
    """

    selected_trailing_icon: IconDataOrControl = Icons.ARROW_DROP_UP
    """
    An optional icon at the end of the text field to indicate that the text field is
    pressed.
    """

    bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    The background color of the dropdown menu
    in various [`ControlState`][flet.ControlState]
    states.
    """

    on_change: Optional[ControlEventHandler["Dropdown"]] = None
    """
    Called when the selected item of this dropdown has changed.
    """

    on_focus: Optional[ControlEventHandler["Dropdown"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["Dropdown"]] = None
    """
    Called when the control has lost focus.
    """

    # From FormField

    error_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] to use for
    [`error_text`][flet.Dropdown.error_text].
    """

    error_text: Optional[str] = None
    """
    Text that appears below the input border.

    If non-null, the border's color animates to red and the `helper_text` is not shown.
    """

    text_size: Optional[Number] = None
    """
    Text size in virtual pixels.
    """

    text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] to use for text
    in input text field.
    """

    label: Optional[StrOrControl] = None
    """
    Optional text that describes the input field.

    When the input field is empty and unfocused, the label is displayed on top of the
    input field (i.e., at the same location on the screen where text may be entered in
    the input field). When the input field receives focus (or if the field is
    non-empty) the label moves above, either vertically adjacent to, or to the center
    of the input field.
    """

    label_style: Optional[TextStyle] = None
    """
    The [`label`][flet.Dropdown.label]'s text style.
    """

    border: Optional[InputBorder] = None
    """
    Border around input.

    Defaults to `InputBorder.OUTLINE`.
    """

    color: Optional[ColorValue] = None
    """
    Text color.
    """

    border_width: Number = 1
    """
    The width of the border in virtual pixels. Set to `0` to completely remove border.
    """

    border_color: Optional[ColorValue] = None
    """
    Border color. Could be `transparent` to
    hide the border.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    """

    focused_border_width: Optional[Number] = None
    """
    Border width in focused state.
    """

    focused_border_color: Optional[ColorValue] = None
    """
    Border color in focused state.
    """

    content_padding: Optional[PaddingValue] = None
    """
    The padding for the input decoration's container.
    """

    dense: bool = False
    """
    Whether the TextField is part of a dense form (i.e., uses less vertical space).
    """

    filled: bool = False
    """
    Whether the decoration's container is filled with theme
    [`fill_color`][flet.Dropdown.fill_color].
    """

    fill_color: Optional[ColorValue] = None
    """
    Background color of the dropdown input
    text field.

    Note:
        Will not be visible if `filled=False`.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color of the dropdown input text
    field when hovered.
    """

    hint_text: Optional[str] = None
    """
    Text that suggests what sort of input the field accepts.

    Displayed on top of the input when it's empty and either (a) `label` is null or (b)
    the input has the focus.
    """

    hint_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] to use for
    [`hint_text`][flet.Dropdown.hint_text].
    """

    helper_text: Optional[str] = None
    """
    Text that provides context about the input's value, such as how the value will be
    used.

    If non-null, the text is displayed below the input decorator, in the same location
    as `error_text`. If a non-null `error_text` value is specified then the helper text
    is not shown.
    """

    helper_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] to use for
    [`helper_text`][flet.Dropdown.helper_text].
    """

    def before_update(self):
        super().before_update()
        self.expand_loose = self.expand  # to fix a display issue

    def __contains__(self, item):
        return item in self.options

    async def focus(self):
        await self._invoke_method("focus")
