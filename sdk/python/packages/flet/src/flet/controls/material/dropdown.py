import asyncio
from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.material.form_field_control import InputBorder
from flet.controls.material.icons import Icons
from flet.controls.material.textfield import InputFilter, TextCapitalization
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconValueOrControl,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
    TextAlign,
)

__all__ = ["Dropdown", "DropdownOption"]


@control("Option")
class Option(Control):
    """
    Represents an item in a dropdown. Either `key` or `text` must be specified, else an
    `AssertionError` will be raised.
    """

    key: Optional[str] = None
    """
    Option's key. If not specified `text` will be used as fallback.
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

    leading_icon: Optional[IconValueOrControl] = None
    """
    An optional icon to display before the content or text.
    """

    trailing_icon: Optional[IconValueOrControl] = None
    """
    An optional icon to display after the content or text.
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this menu item's appearance. 

    The value is an instance of [`ButtonStyle`](https://flet.dev/docs/reference/types/buttonstyle) 
    class. 
    """

    def before_update(self):
        super().before_update()
        assert self.key is not None or self.text is not None, (
            "key or text must be specified"
        )


DropdownOption = Option


@control("Dropdown")
class Dropdown(ConstrainedControl):
    """
    A dropdown control that allows users to select a single option from a list of
    options.

    Online docs: https://flet.dev/docs/controls/dropdown
    """

    value: Optional[str] = None
    """
    `key` value of the selected option.
    """

    options: list[Option] = field(default_factory=list)
    """
    A list of `DropdownOption` controls representing items in this dropdown.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than 
    one control on a page with autofocus set, then the first one added to the page will 
    get focus.
    """

    text_align: TextAlign = TextAlign.START
    """
    The text align for the TextField of the Dropdown.

    Value is of type [`TextAlign`](https://flet.dev/docs/reference/types/textalign) and 
    defaults to `TextAlign.START`.
    """

    elevation: Optional[ControlStateValue[OptionalNumber]] = 8
    """
    The dropdown's menu elevation in various [`ControlState`](https://flet.dev/docs/reference/types/controlstate) 
    states.

    Defaults to `8`.
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

    Defaults to true as the search function could be commonly used.
    """

    editable: bool = False
    """
    TBD
    """

    menu_height: OptionalNumber = None
    """
    The height of the dropdown menu. If this is null, the menu will display as many 
    items as possible on the screen.
    """

    menu_width: OptionalNumber = None
    """
    The width of the dropdown menu. If this is null, the menu width will be the same as 
    input textfield width.
    """

    expanded_insets: OptionalPaddingValue = None
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

    trailing_icon: IconValueOrControl = Icons.ARROW_DROP_DOWN
    """
    An optional icon at the end of the text field (previously, 
    [`select_icon`](#select_icon)).

    Defaults to an Icon with `ft.Icons.ARROW_DROP_DOWN`.
    """

    leading_icon: Optional[IconValueOrControl] = None
    """
    An optional Icon at the front of the text input field inside the decoration box 
    (previously, [`prefix_icon`](#prefix_icon)).

    Defaults to null. If this is not null, the menu items will have extra paddings to 
    be aligned with the text in the text field.
    """

    selected_trailing_icon: IconValueOrControl = Icons.ARROW_DROP_UP
    """
    An optional icon at the end of the text field to indicate that the text field is 
    pressed.

    Defaults to an Icon with `ft.Icons.ARROW_DROP_UP`.
    """

    bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    The background [color](https://flet.dev/docs/reference/colors) of the dropdown menu 
    in various [`ControlState`](https://flet.dev/docs/reference/types/controlstate) 
    states.
    """

    on_change: OptionalControlEventHandler["Dropdown"] = None
    """
    Fires when the selected item of this dropdown has changed.
    """

    on_focus: OptionalControlEventHandler["Dropdown"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["Dropdown"] = None
    """
    Fires when the control has lost focus.
    """

    # From FormField

    error_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `error_text`.
    """

    error_text: Optional[str] = None
    """
    Text that appears below the input border.

    If non-null, the border's color animates to red and the `helper_text` is not shown.
    """

    text_size: OptionalNumber = None
    """
    Text size in virtual pixels.
    """

    text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for text 
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
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `label`.
    """

    border: Optional[InputBorder] = None
    """
    Border around input.

    Value is of type [`InputBorder`](https://flet.dev/docs/reference/types/inputborder) 
    and defaults to `InputBorder.OUTLINE`.
    """

    color: OptionalColorValue = None
    """
    Text [color](https://flet.dev/docs/reference/colors).
    """

    border_width: Number = 1
    """
    The width of the border in virtual pixels. Set to `0` to completely remove border.

    Defaults to `1`.
    """

    border_color: OptionalColorValue = None
    """
    Border [color](https://flet.dev/docs/reference/colors). Could be `transparent` to 
    hide the border.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Border radius is an instance of [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius) 
    class.
    """

    focused_border_width: OptionalNumber = None
    """
    Border width in focused state.
    """

    focused_border_color: OptionalColorValue = None
    """
    Border [color](https://flet.dev/docs/reference/colors) in focused state.
    """

    content_padding: OptionalPaddingValue = None
    """
    The [padding](https://flet.dev/docs/reference/types/padding) for the input 
    decoration's container.
    """

    dense: bool = False
    """
    Whether the TextField is part of a dense form (ie, uses less vertical space).
    """

    filled: bool = False
    """
    If `True` the decoration's container is filled with theme `fill_color`. The default 
    is `False`.
    """

    fill_color: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of the dropdown input 
    text field. Will not be visible if `filled=False`.
    """

    hover_color: OptionalColorValue = None
    """
    TBD
    """

    hint_text: Optional[str] = None
    """
    Text that suggests what sort of input the field accepts.

    Displayed on top of the input when it's empty and either (a) `label` is null or (b) 
    the input has the focus.
    """

    hint_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `hint_text`.
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
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `helper_text`.
    """

    def before_update(self):
        super().before_update()
        self.expand_loose = self.expand  # to fix a display issue

    def __contains__(self, item):
        return item in self.options

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
