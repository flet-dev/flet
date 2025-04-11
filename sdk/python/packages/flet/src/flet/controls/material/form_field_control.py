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
    OptionalString,
    StrOrControl,
    VerticalAlignment,
)
from flet.utils.deprecated import deprecated_warning


class InputBorder(Enum):
    NONE = "none"
    OUTLINE = "outline"
    UNDERLINE = "underline"


@control(kw_only=True)
class FormFieldControl(ConstrainedControl):
    text_size: OptionalNumber = None
    text_style: Optional[TextStyle] = None
    text_vertical_align: Union[VerticalAlignment, OptionalNumber] = None
    label: Optional[StrOrControl] = None
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
    hint_text: OptionalString = None
    hint_style: Optional[TextStyle] = None
    hint_fade_duration: OptionalDurationValue = None
    hint_max_lines: Optional[int] = None
    helper: Optional[StrOrControl] = None
    helper_text: OptionalString = None  # todo(0.73.0): remove in favor of helper
    helper_style: Optional[TextStyle] = None
    helper_max_lines: Optional[int] = None
    counter: Optional[StrOrControl] = None
    counter_text: OptionalString = None  # todo(0.73.0): remove in favor of counter
    counter_style: Optional[TextStyle] = None
    error: Optional[StrOrControl] = None
    error_text: OptionalString = None  # todo(0.73.0): remove in favor of error
    error_style: Optional[TextStyle] = None
    error_max_lines: Optional[int] = None
    prefix: Optional[StrOrControl] = None
    prefix_icon: Optional[IconValueOrControl] = None
    prefix_icon_size_constraints: Optional[BoxConstraints] = None
    prefix_text: OptionalString = None  # todo(0.73.0): remove in favor of prefix
    prefix_style: Optional[TextStyle] = None
    suffix: Optional[StrOrControl] = None
    suffix_icon: Optional[IconValueOrControl] = None
    suffix_icon_size_constraints: Optional[BoxConstraints] = None
    size_constraints: Optional[BoxConstraints] = None
    collapsed: Optional[bool] = None
    fit_parent_size: Optional[bool] = None
    suffix_text: OptionalString = None  # todo(0.73.0): remove in favor of suffix
    suffix_style: Optional[TextStyle] = None

    def __setattr__(self, name, value):
        if name == "suffix_text" and value is not None:
            deprecated_warning(
                name=name,
                reason="Use suffix instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        if name == "prefix_text" and value is not None:
            deprecated_warning(
                name=name,
                reason="Use prefix instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        if name == "error_text" and value is not None:
            deprecated_warning(
                name=name,
                reason="Use error instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        if name == "counter_text" and value is not None:
            deprecated_warning(
                name=name,
                reason="Use counter instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        if name == "helper_text" and value is not None:
            deprecated_warning(
                name=name,
                reason="Use helper instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        super().__setattr__(name, value)
