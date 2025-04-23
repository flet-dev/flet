import asyncio
from dataclasses import dataclass, field
from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_state import OptionalControlStateValue
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
    OptionalEventCallable,
    OptionalNumber,
    StrOrControl,
    TextAlign,
)

__all__ = ["Dropdown", "DropdownOption"]


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
class Dropdown(ConstrainedControl):
    """
    A dropdown control that allows users to select a single option from a list of options.

    Online docs: https://flet.dev/docs/controls/dropdown
    """

    value: Optional[str] = None
    options: List[Option] = field(default_factory=list)
    autofocus: bool = False
    text_align: TextAlign = TextAlign.START
    elevation: OptionalControlStateValue[OptionalNumber] = 8
    enable_filter: bool = False
    enable_search: bool = True
    editable: bool = False
    menu_height: OptionalNumber = None
    menu_width: OptionalNumber = None
    expanded_insets: OptionalPaddingValue = None
    selected_suffix: Optional[Control] = None
    input_filter: Optional[InputFilter] = None
    capitalization: Optional[TextCapitalization] = None
    trailing_icon: IconValueOrControl = Icons.ARROW_DROP_DOWN
    leading_icon: Optional[IconValueOrControl] = None
    selected_trailing_icon: IconValueOrControl = Icons.ARROW_DROP_UP
    bgcolor: OptionalControlStateValue[ColorValue] = None
    on_change: OptionalEventCallable = None
    on_focus: OptionalEventCallable = None
    on_blur: OptionalEventCallable = None

    # From FormField
    error_style: Optional[TextStyle] = None
    error_text: Optional[str] = None
    text_size: OptionalNumber = None
    text_style: Optional[TextStyle] = None
    label: Optional[StrOrControl] = None
    label_style: Optional[TextStyle] = None
    border: Optional[InputBorder] = None
    color: OptionalColorValue = None
    border_width: Number = 1
    border_color: OptionalColorValue = None
    border_radius: OptionalBorderRadiusValue = None
    focused_border_width: OptionalNumber = None
    focused_border_color: OptionalColorValue = None
    content_padding: OptionalPaddingValue = None
    dense: bool = False
    filled: bool = False
    fill_color: OptionalColorValue = None
    hover_color: OptionalColorValue = None
    hint_text: Optional[str] = None
    hint_style: Optional[TextStyle] = None
    helper_text: Optional[str] = None
    helper_style: Optional[TextStyle] = None

    def before_update(self):
        super().before_update()
        self.expand_loose = self.expand  # to fix a display issue

    def __contains__(self, item):
        return item in self.options

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
