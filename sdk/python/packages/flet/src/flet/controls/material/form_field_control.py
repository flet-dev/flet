from enum import Enum
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.box import BoxConstraints
from flet.controls.duration import DurationValue
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
    VerticalAlignment,
)


class InputBorder(Enum):
    NONE = "none"
    OUTLINE = "outline"
    UNDERLINE = "underline"


@control(kw_only=True)
class FormFieldControl(LayoutControl):
    text_size: Optional[Number] = None
    """
    Text size in virtual pixels.
    """

    text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.] to use for the
    text being edited.
    """

    text_vertical_align: Optional[Union[VerticalAlignment, Number]] = None
    """
    Defines how the text should be aligned vertically.

    Value can either be a number ranging from `-1.0` (topmost location) to `1.0`
    (bottommost location) or of type [`VerticalAlignment`][flet.]
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
    The text style to use for `label`.
    """

    icon: Optional[IconDataOrControl] = None
    """
    The icon to show before the input field and outside of the decoration's container.
    """

    border: InputBorder = InputBorder.OUTLINE
    """
    Border around input.
    """

    color: Optional[ColorValue] = None
    """
    Text color.
    """

    bgcolor: Optional[ColorValue] = None
    """
    TextField background color.

    Note:
        Will not be visible if [`filled`][flet.FormFieldControl.] is `False`.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    """

    border_width: Optional[Number] = None
    """
    The width of the border in virtual pixels.

    Defaults to `1`.

    Tip:
        Set to `0` to completely remove the border.
    """

    border_color: Optional[ColorValue] = None
    """
    The border color.

    Tip:
        Set to [`Colors.TRANSPARENT`][flet.] to invisible/hide the border.
    """

    focused_color: Optional[ColorValue] = None
    """
    The text's color when focused.
    """

    focused_bgcolor: Optional[ColorValue] = None
    """
    Background color in focused state.

    Note:
        Will not be visible if [`filled`][flet.FormFieldControl.] is `False`.
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

    dense: Optional[bool] = None
    """
    Whether this control is part of a dense form (ie, uses less vertical space).
    """

    filled: Optional[bool] = None
    """
    If `True` the decoration's container is filled with theme
    [`fill_color`][flet.FormFieldControl.].

    If `filled=None` (the default), then it is implicitly set to `True` when at least
    one of the following is not `None`: [`fill_color`][flet.FormFieldControl.],
    [`focused_bgcolor`][flet.FormFieldControl.],
    [`hover_color`][flet.FormFieldControl.] and [`bgcolor`][flet.FormFieldControl.].
    """

    fill_color: Optional[ColorValue] = None
    """
    Background color of TextField.

    Note:
        Will not be visible if [`filled`][flet.FormFieldControl.] is `False`.
    """

    focus_color: Optional[ColorValue] = None
    """
    TBD
    """

    align_label_with_hint: Optional[bool] = None
    """
    TBD
    """

    hover_color: Optional[ColorValue] = None
    """
    Background color of TextField when hovered.

    Note:
        Will not be visible if [`filled`][flet.FormFieldControl.] is `False`.
    """

    hint_text: Optional[str] = None
    """
    Text that suggests what sort of input the field accepts.

    Displayed on top of the input when the it's empty and either
    (a) [`label`][flet.FormFieldControl.] is `None` or (b) the input has the focus.
    """

    hint_style: Optional[TextStyle] = None
    """
    The text style to use for [`hint_text`][flet.FormFieldControl.].
    """

    hint_fade_duration: Optional[DurationValue] = None
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
    as [`error`][flet.FormFieldControl.]. If a non-null
    [`error`][flet.FormFieldControl.] value is specified then the helper text is not
    shown.
    """

    helper_style: Optional[TextStyle] = None
    """
    The text style to use for [`helper`][flet.FormFieldControl.].
    """

    helper_max_lines: Optional[int] = None
    """
    TBD
    """

    counter: Optional[StrOrControl] = None
    """
    A `Control` to place below the line as a character count.

    If `None` or an empty string then nothing will appear in the counter's location.
    """

    counter_style: Optional[TextStyle] = None
    """
    The text style to use for `counter`.
    """

    error: Optional[StrOrControl] = None
    """
    Text that appears below the input border.

    If non-null, the border's color animates to red
    and the [`helper`][flet.FormFieldControl.] is not shown.
    """

    error_style: Optional[TextStyle] = None
    """
    The text style to use for [`error`][flet.FormFieldControl.].
    """

    error_max_lines: Optional[int] = None
    """
    TBD
    """

    prefix: Optional[StrOrControl] = None
    """
    A `Control` to place on the line before the input.

    It appears after the [`prefix_icon`][flet.FormFieldControl.], if both are specified.

    This can be used, for example, to add some padding to text that would otherwise be
    specified using `prefix`, or to add a custom control in front of the input.
    The control's baseline is lined up with the input baseline.
    """

    prefix_icon: Optional[IconDataOrControl] = None
    """
    An icon that appears before the editable part of the text field,
    within the decoration's container.

    If [`prefix`][flet.FormFieldControl.] is specified and visible,
    this icon will appear to its left.
    """

    prefix_icon_size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    prefix_style: Optional[TextStyle] = None
    """
    The text style to use for [`prefix`][flet.FormFieldControl.].
    """

    suffix: Optional[StrOrControl] = None
    """
    A `Control` to place on the line after the input.

    It appears before the [`suffix_icon`][flet.FormFieldControl.],
    if both are specified.

    This can be used, for example, to add some padding to the text that would otherwise
    be specified using `suffix`, or to add a custom control after the input.
    The control's baseline is lined up with the input baseline.
    """

    suffix_icon: Optional[IconDataOrControl] = None
    """
    An icon that appears after the editable part of the text field and after the
    [`suffix`][flet.FormFieldControl.], within the decoration's container.
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
    The text style to use for [`suffix`][flet.FormFieldControl.].
    """

    async def focus(self):
        """
        Request focus for this control.

        Example:
            ```python
            async def main(page: ft.Page):
                page.add(ctf := ft.TextField())
                await ctf.focus()
            ```
        """
        await self._invoke_method("focus")
