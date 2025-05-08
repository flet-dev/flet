import asyncio
from dataclasses import field
from enum import Enum
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.box import BoxConstraints
from flet.controls.constrained_control import ConstrainedControl
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


class InputBorder(Enum):
    NONE = "none"
    OUTLINE = "outline"
    UNDERLINE = "underline"


@control(kw_only=True)
class FormFieldControl(ConstrainedControl):
    text_size: OptionalNumber = None
    """
    Text size in virtual pixels.
    """

    text_style: TextStyle = field(default_factory=lambda: TextStyle())
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for the 
    text being edited.
    """

    text_vertical_align: Union[VerticalAlignment, OptionalNumber] = None
    """
    Defines how the text should be aligned vertically.

    Value can either be a number ranging from `-1.0` (topmost location) to `1.0` 
    (bottommost location) or of type [`VerticalAlignment`](https://flet.dev/docs/reference/types/verticalalignment). 
    Defaults to `VerticalAlignment.CENTER`.
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

    icon: Optional[IconValueOrControl] = None
    """
    The icon to show before the input field and outside of the decoration's container. 
    Can be a `Control` or an icon name.
    """

    border: InputBorder = InputBorder.OUTLINE
    """
    Border around input.

    Value is of type [`InputBorder`](https://flet.dev/docs/reference/types/inputborder) 
    and defaults to `InputBorder.OUTLINE`.
    """

    color: OptionalColorValue = None
    """
    Text [color](https://flet.dev/docs/reference/colors).
    """

    bgcolor: OptionalColorValue = None
    """
    TextField background [color](https://flet.dev/docs/reference/colors). Will not be 
    visible if `filled=False`.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Border radius is an instance of [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius) 
    class.
    """

    border_width: OptionalNumber = None
    """
    The width of the border in virtual pixels. Set to `0` to completely remove the 
    border.

    Defaults to `1`.
    """

    border_color: OptionalColorValue = None
    """
    Border [color](https://flet.dev/docs/reference/colors). Could be `transparent` to 
    hide the border.
    """

    focused_color: OptionalColorValue = None
    """
    Text [color](https://flet.dev/docs/reference/colors) when TextField is focused.
    """

    focused_bgcolor: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of TextField in focused 
    state. Will not be visible if `filled=False`.
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
    The padding for the input decoration's container.

    The value is an instance of [`padding.Padding`](https://flet.dev/docs/reference/types/padding) 
    class or a number.
    """

    dense: Optional[bool] = None
    """
    Whether the TextField is part of a dense form (ie, uses less vertical space).
    """

    filled: Optional[bool] = None
    """
    If `True` the decoration's container is filled with theme `fill_color`.

    If `filled=None`(default), then it is implicitly set to `True` when at least one of 
    the following is not `None`: `fill_color`, `focused_bgcolor`, `hover_color` and 
    `bgcolor`.
    """

    fill_color: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of TextField. Will not 
    be visible if `filled=False`.
    """

    focus_color: OptionalColorValue = None
    """
    TBD
    """

    align_label_with_hint: Optional[bool] = None
    """
    TBD
    """

    hover_color: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of TextField when 
    hovered. Will not be visible if `filled=False`.
    """

    hint_text: OptionalString = None
    """
    Text that suggests what sort of input the field accepts.

    Displayed on top of the input when the it's empty and either (a) `label` is null or 
    (b) the input has the focus.
    """

    hint_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `hint_text`.
    """

    hint_fade_duration: OptionalDurationValue = None
    """
    TBD
    """

    hint_max_lines: Optional[int] = None
    """
    TBD
    """

    helper: Optional[StrOrControl] = None
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

    helper_max_lines: Optional[int] = None
    """
    TBD
    """

    counter: Optional[StrOrControl] = None
    """
    A `Control` to place below the line as a character count.

    If `None` or an empty string and `counter_text` isn't specified, then nothing will 
    appear in the counter's location.
    """

    counter_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `counter_text`.
    """

    error: Optional[StrOrControl] = None
    """
    Text that appears below the input border.

    If non-null, the border's color animates to red and the `helper_text` is not shown.
    """

    error_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `error_text`.
    """

    error_max_lines: Optional[int] = None
    """
    TBD
    """

    prefix: Optional[StrOrControl] = None
    """
    Optional `Control` to place on the line before the input.

    This can be used, for example, to add some padding to text that would otherwise be 
    specified using `prefix_text`, or to add a custom control in front of the input. 
    The control's baseline is lined up with the input baseline.

    Only one of `prefix` and `prefix_text` can be specified.

    The `prefix` appears after the `prefix_icon`, if both are specified.
    """

    prefix_icon: Optional[IconValueOrControl] = None
    """
    An icon that appears before the `prefix` or `prefix_text` and before the editable 
    part of the text field, within the decoration's container. Can be a `Control` or an 
    icon name.
    """

    prefix_icon_size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    prefix_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `prefix_text`.
    """

    suffix: Optional[StrOrControl] = None
    """
    Optional `Control` to place on the line after the input.

    This can be used, for example, to add some padding to the text that would otherwise 
    be specified using `suffix_text`, or to add a custom control after the input. 
    The control's baseline is lined up with the input baseline.

    Only one of `suffix` and `suffix_text` can be specified.

    The `suffix` appears before the `suffix_icon`, if both are specified.
    """

    suffix_icon: Optional[IconValueOrControl] = None
    """
    An icon that appears after the editable part of the text field and after the 
    `suffix` or `suffix_text`, within the decoration's container. Can be a `Control` or 
    an icon name.
    """

    suffix_icon_size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    collapsed: Optional[bool] = None
    """
    TBD
    """

    fit_parent_size: Optional[bool] = None
    """
    TBD
    """

    suffix_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to use for 
    `suffix_text`.
    """

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
