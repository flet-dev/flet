from enum import Enum
from typing import Optional, Union

from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.box import BoxConstraints
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.duration import OptionalDurationValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    IconValueOrControl,
    OptionalColorValue,
    OptionalNumber,
    VerticalAlignment,
)


class InputBorder(Enum):
    NONE = "none"
    OUTLINE = "outline"
    UNDERLINE = "underline"


@control(kw_only=True)
class FormFieldControl(ConstrainedControl):
    text_size: OptionalNumber = None
    text_style: Optional[TextStyle] = None
    text_vertical_align: Union[VerticalAlignment, OptionalNumber] = None
    label: Optional[Union[str, Control]] = None
    label_style: Optional[TextStyle] = None
    icon: Optional[IconValueOrControl] = None
    border: Optional[InputBorder] = None
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    border_radius: OptionalBorderRadiusValue = None
    border_width: OptionalNumber = None
    border_color: OptionalColorValue = None
    focused_color: OptionalColorValue = None
    focused_bgcolor: OptionalColorValue = None
    focused_border_width: OptionalNumber = None
    focused_border_color: OptionalColorValue = None
    content_padding: OptionalPaddingValue = None
    dense: Optional[bool] = None
    filled: Optional[bool] = None
    fill_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    align_label_with_hint: Optional[bool] = None
    hover_color: OptionalColorValue = None
    hint_text: Optional[str] = None
    hint_style: Optional[TextStyle] = None
    hint_fade_duration: OptionalDurationValue = None
    hint_max_lines: Optional[int] = None
    helper: Optional[Control] = None
    helper_text: Optional[str] = None
    helper_style: Optional[TextStyle] = None
    helper_max_lines: Optional[int] = None
    counter: Optional[Control] = None
    counter_text: Optional[str] = None
    counter_style: Optional[TextStyle] = None
    error: Optional[Control] = None
    error_text: Optional[str] = None
    error_style: Optional[TextStyle] = None
    error_max_lines: Optional[int] = None
    prefix: Optional[Control] = None
    prefix_icon: Optional[IconValueOrControl] = None
    prefix_icon_size_constraints: Optional[BoxConstraints] = None
    prefix_text: Optional[str] = None
    prefix_style: Optional[TextStyle] = None
    suffix: Optional[Control] = None
    suffix_icon: Optional[IconValueOrControl] = None
    suffix_icon_size_constraints: Optional[BoxConstraints] = None
    size_constraints: Optional[BoxConstraints] = None
    collapsed: Optional[bool] = None
    fit_parent_size: Optional[bool] = None
    suffix_text: Optional[str] = None
    suffix_style: Optional[TextStyle] = None
