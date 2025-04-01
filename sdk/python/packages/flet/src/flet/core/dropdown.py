from dataclasses import dataclass, field
from typing import List, Optional, Union

from flet.core.buttons import ButtonStyle
from flet.core.control import Control, OptionalNumber, control
from flet.core.form_field_control import FormFieldControl, InputBorder
from flet.core.icons import Icons
from flet.core.text_style import TextStyle
from flet.core.textfield import InputFilter, TextCapitalization
from flet.core.types import (
    BorderRadiusValue,
    ColorValue,
    ControlStateValue,
    IconValueOrControl,
    OptionalEventCallable,
    PaddingValue,
    TextAlign,
)


@control("Option")
class Option(Control):

    key: Optional[str] = None
    text: Optional[str] = None
    content: Optional[Control] = None
    leading_icon: Optional[IconValueOrControl] = None
    trailing_icon: Optional[IconValueOrControl] = None
    style: Optional[ButtonStyle] = None

    def before_update(self):
        super().before_update()
        assert (
            self.key is not None or self.text is not None
        ), "key or text must be specified"


@dataclass
class DropdownOption(Option):
    """Alias for Option"""


@control("Dropdown")
class Dropdown(FormFieldControl):
    """
    A dropdown control that allows users to select a single option from a list of options.
    -----
    Online docs: https://flet.dev/docs/controls/dropdown
    """

    value: Optional[str] = None
    autofocus: Optional[bool] = field(default=False)
    text_align: Optional[TextAlign] = field(default=TextAlign.START)
    elevation: ControlStateValue[OptionalNumber] = field(default=8)
    options: Optional[List[Option]] = None
    label_content: Optional[str] = None
    enable_filter: Optional[bool] = field(default=False)
    enable_search: Optional[bool] = field(default=True)
    editable: Optional[bool] = field(default=False)
    menu_height: OptionalNumber = None
    menu_width: OptionalNumber = None
    expanded_insets: PaddingValue = None
    selected_suffix: Optional[Control] = None
    input_filter: Optional[InputFilter] = None
    capitalization: Optional[TextCapitalization] = None
    trailing_icon: Optional[IconValueOrControl] = field(default=Icons.ARROW_DROP_DOWN)
    leading_icon: Optional[IconValueOrControl] = None
    selected_trailing_icon: Optional[IconValueOrControl] = field(
        default=Icons.ARROW_DROP_UP
    )
    bgcolor: ControlStateValue[ColorValue] = None
    on_change: OptionalEventCallable = None
    on_focus: OptionalEventCallable = None
    on_blur: OptionalEventCallable = None

    # From FormField
    error_style: Optional[TextStyle] = None
    error_text: Optional[str] = None
    text_size: OptionalNumber = None
    text_style: Optional[TextStyle] = None
    label: Optional[Union[str, Control]] = None
    label_style: Optional[TextStyle] = None
    border: Optional[InputBorder] = None
    color: Optional[ColorValue] = None
    border_width: OptionalNumber = field(default=1)
    border_color: Optional[ColorValue] = None
    border_radius: Optional[BorderRadiusValue] = None
    focused_border_width: OptionalNumber = None
    focused_border_color: Optional[ColorValue] = None
    content_padding: Optional[PaddingValue] = None
    dense: Optional[bool] = field(default=False)
    filled: Optional[bool] = field(default=False)
    fill_color: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    hint_text: Optional[str] = None
    hint_style: Optional[TextStyle] = None
    helper_text: Optional[str] = None
    helper_style: Optional[TextStyle] = None

    def before_update(self):
        super().before_update()
        self.expand_loose = self.expand  # to fix a display issue

    def __contains__(self, item):
        return item in self.__options

    def focus(self):
        # TODO
        pass
