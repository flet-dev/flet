from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.buttons import ButtonStyle
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.material.form_field_control import InputBorder
from flet.controls.material.menu_bar import MenuStyle
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
    Represents an item in a dropdown.
    """

    key: Optional[str] = None
    """
    Option's key.

    If not specified [`text`][(c).] will be used as fallback.

    Raises:
        ValueError: If neither `key` nor [`text`][(c).] are provided.
    """

    text: Optional[str] = None
    """
    Option's display text.

    If not specified [`key`][(c).] will be used as fallback.

    Raises:
        ValueError: If neither [`key`][(c).] nor `text` are provided.
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
        if self.key is None and self.text is None:
            raise ValueError("key or text must be specified")


Option = DropdownOption


@control("Dropdown")
class Dropdown(LayoutControl):
    """
    A dropdown control that allows users to select a single option
    from a list of [`options`][(c).].

    Example:
    ```python
    ft.Dropdown(
        width=220,
        value="alice",
        options=[
            ft.DropdownOption(key="alice", text="Alice"),
            ft.DropdownOption(key="bob", text="Bob"),
        ],
    )
    ```
    """

    value: Optional[str] = None
    """
    The [`key`][flet.DropdownOption.] of the dropdown [`options`][(c).]
    corresponding to the selected option.
    """

    options: list[DropdownOption] = field(default_factory=list)
    """
    A list of options to display in the dropdown.
    """

    text: Optional[str] = None
    """
    The text entered in the text field.
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
    The dropdown's menu elevation in various [`ControlState`][flet.]
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
    Whether the dropdown allows editing of the text input field.
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

    menu_style: Optional[MenuStyle] = None
    """
    The menu style that defines the visual attributes of the menu.

    The default width of the menu is set to the width of the text field.
    """

    expanded_insets: Optional[PaddingValue] = None
    """
    The insets for the expanded dropdown menu.
    """

    selected_suffix: Optional[Control] = None
    """
    A control to display after the selected item in the dropdown.
    """

    input_filter: Optional[InputFilter] = None
    """
    A filter to apply to the text input field.
    """

    capitalization: Optional[TextCapitalization] = None
    """
    Configures how the text input should be capitalized.
    """

    trailing_icon: Optional[IconDataOrControl] = None
    """
    An icon to display at the end of the text field.
    """

    leading_icon: Optional[IconDataOrControl] = None
    """
    An optional Icon at the front of the text input field inside the decoration box.

    If this is not null, the menu items will have extra paddings to
    be aligned with the text in the text field.
    """

    selected_trailing_icon: Optional[IconDataOrControl] = None
    """
    An optional icon at the end of the text field to indicate that the text field is
    pressed.
    """

    bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    The background color of the dropdown menu
    in various [`ControlState`][flet.]
    states.
    """

    on_select: Optional[ControlEventHandler["Dropdown"]] = None
    """
    Called when the selected item of this dropdown has changed.
    """

    on_text_change: Optional[ControlEventHandler["Dropdown"]] = None
    """
    Called when the [`text`][(c).] input of this dropdown has changed.
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
    The [`TextStyle`][flet.] to use for
    [`error_text`][(c).].
    """

    error_text: Optional[str] = None
    """
    Text that appears below the input border.

    If non-null, the border's color animates to red and the [`helper_text`][(c).] is
    not shown.
    """

    text_size: Optional[Number] = None
    """
    Text size in virtual pixels.
    """

    text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.] to use for text
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
    The [`label`][(c).]'s text style.
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
    The width of the border in virtual pixels.

    Tip:
        Set to `0` to completely remove the border.
    """

    border_color: Optional[ColorValue] = None
    """
    Border color.

    Tip:
        Set to [`Colors.TRANSPARENT`][flet.] to hide the border.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The border radius applied to the corners of the dropdown input field.
    Accepts a value in virtual pixels or a `BorderRadiusValue` object.
    If set to `None`, the default border radius defined by the theme or system is used.
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
    [`fill_color`][(c).].
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
    The [`TextStyle`][flet.] to use for
    [`hint_text`][(c).].
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
    The [`TextStyle`][flet.] to use for
    [`helper_text`][(c).].
    """

    def __contains__(self, item):
        return item in self.options

    async def focus(self):
        """Requests focus for this control."""
        await self._invoke_method("focus")
