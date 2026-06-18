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
    """
    Border styles supported by :class:`~flet.FormFieldControl`.

    These values select the border style drawn around the decorated input area.
    """

    NONE = "none"
    """
    Draws no border around the decoration's container.
    """

    OUTLINE = "outline"
    """
    Draws a border around all sides of the decoration's container.
    """

    UNDERLINE = "underline"
    """
    Draws a horizontal line along the bottom edge of the decoration's container.
    """


@control(kw_only=True)
class FormFieldControl(LayoutControl):
    """
    Base class for Material form-field controls with a decorated input area.

    It provides the shared label, hint, helper, error, prefix, suffix, fill, and
    border properties used by controls such as :class:`~flet.TextField` and
    :class:`~flet.DropdownM2`.
    """

    text_size: Optional[Number] = None
    """
    Text size in virtual pixels.
    """

    text_style: Optional[TextStyle] = None
    """
    The :class:`~flet.TextStyle` to use for the text being edited.
    """

    text_vertical_align: Optional[Union[VerticalAlignment, Number]] = None
    """
    Defines how the text should be aligned vertically.

    Value can either be a number ranging from `-1.0` (topmost location) to `1.0`
    (bottommost location) or of type :class:`~flet.VerticalAlignment`
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
        Will not be visible if :attr:`filled` is `False`.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    Rounds the corners of the outlined decoration border.

    Note:
        This is applied when :attr:`border` uses an outlined
        border. Underline and borderless variants do not visibly use this radius.
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
        Set to :attr:`flet.Colors.TRANSPARENT` to invisible/hide the border.
    """

    focused_color: Optional[ColorValue] = None
    """
    The text's color when focused.
    """

    focused_bgcolor: Optional[ColorValue] = None
    """
    Background color in focused state.

    Note:
        Will not be visible if :attr:`filled` is `False`.
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
    Whether the decoration's container is filled with :attr:`fill_color`.

    If `filled=None` (the default), then it is implicitly set to `True` when at least
    one of the following is not `None`: :attr:`fill_color`,
    :attr:`focused_bgcolor`, :attr:`hover_color`, and :attr:`bgcolor`.
    """

    fill_color: Optional[ColorValue] = None
    """
    Background color of TextField.

    Note:
        Will not be visible if :attr:`filled` is `False`.
    """

    focus_color: Optional[ColorValue] = None
    """
    The fill color of the decoration's container when the control has input focus.

    Note:
        Text fields usually indicate focus by changing the focused border instead of
        the fill color. In Flet, prefer :attr:`focused_bgcolor` and
        :attr:`focused_border_color` when you need explicit
        focused-state styling.
    """

    align_label_with_hint: Optional[bool] = None
    """
    Whether the floating label should align with :attr:`hint_text`.

    This is typically set to `True` for multiline text input to align the label with
    the top of the hint instead of centering it vertically.
    """

    hover_color: Optional[ColorValue] = None
    """
    Background color of TextField when hovered.

    Note:
        Will not be visible if :attr:`filled` is `False`.
    """

    hint_text: Optional[str] = None
    """
    Text that suggests what sort of input the field accepts.

    Displayed on top of the input when the it's empty and either
    (a) :attr:`label` is `None` or (b) the input has the focus.
    """

    hint_style: Optional[TextStyle] = None
    """
    The text style to use for :attr:`hint_text`.
    """

    hint_fade_duration: Optional[DurationValue] = None
    """
    The duration of the :attr:`hint_text` fade-in and fade-out
    animations.
    """

    hint_max_lines: Optional[int] = None
    """
    The maximum number of lines the :attr:`hint_text` can occupy.
    """

    helper: Optional[StrOrControl] = None
    """
    Text that provides context about the input's value, such as how the value will be \
    used.

    If non-null, the text is displayed below the input decorator, in the same location
    as :attr:`error`. If a non-null :attr:`error` value is specified then the helper
    text is not shown.
    """

    helper_style: Optional[TextStyle] = None
    """
    The text style to use for :attr:`helper`.
    """

    helper_max_lines: Optional[int] = None
    """
    The maximum number of lines the :attr:`helper` can occupy.
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
    and the :attr:`helper` is not shown.
    """

    error_style: Optional[TextStyle] = None
    """
    The text style to use for :attr:`error`.
    """

    error_max_lines: Optional[int] = None
    """
    The maximum number of lines the :attr:`error` can occupy.

    By default, soft line breaks are truncated with an ellipsis while explicit line
    breaks are respected. Set this property to allow long error text to wrap.
    """

    prefix: Optional[StrOrControl] = None
    """
    A `Control` to place on the line before the input.

    It appears after the :attr:`prefix_icon`, if both are specified.

    This can be used, for example, to add some padding to text that would otherwise be
    specified using `prefix`, or to add a custom control in front of the input.
    The control's baseline is lined up with the input baseline.
    """

    prefix_icon: Optional[IconDataOrControl] = None
    """
    An icon that appears before the editable part of the text field, within the \
    decoration's container.

    If :attr:`prefix` is specified and visible,
    this icon will appear to its left.
    """

    prefix_icon_size_constraints: Optional[BoxConstraints] = None
    """
    Size constraints for the area surrounding :attr:`prefix_icon`.

    This can be used to shrink or expand the default icon box. By default, the minimum
    width and height are `48` pixels, and tighter constraints are commonly used
    together with a dense decoration.
    """

    prefix_style: Optional[TextStyle] = None
    """
    The text style to use for :attr:`prefix`.
    """

    suffix: Optional[StrOrControl] = None
    """
    A `Control` to place on the line after the input.

    It appears before the :attr:`suffix_icon`,
    if both are specified.

    This can be used, for example, to add some padding to the text that would otherwise
    be specified using `suffix`, or to add a custom control after the input.
    The control's baseline is lined up with the input baseline.
    """

    suffix_icon: Optional[IconDataOrControl] = None
    """
    An icon that appears after the editable part of the text field and after the \
    :attr:`suffix`, within the decoration's container.
    """

    suffix_icon_size_constraints: Optional[BoxConstraints] = None
    """
    Size constraints for the area surrounding :attr:`suffix_icon`.

    This can be used to shrink or expand the default icon box. By default, the minimum
    width and height are `48` pixels, and tighter constraints are commonly used
    together with a dense decoration.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Defines the minimum and maximum size of the input decorator.
    """

    collapsed: Optional[bool] = None
    """
    Whether the decoration should be the same size as the input field.

    A collapsed decoration removes the extra padding normally added by the decorator.

    Note:
        Collapsed decorations do not support :attr:`label`, :attr:`error`,
        :attr:`counter`, :attr:`icon`, :attr:`prefix`, or :attr:`suffix`.
    """

    fit_parent_size: Optional[bool] = None
    """
    Whether the editable area should expand to fill the height of its parent.

    For controls that support expanding text input, such as
    :class:`~flet.TextField`,
    setting this to `True` expands the editable area to fill the parent and clears the
    line count constraints.

    Note:
        When enabled, :attr:`flet.TextField.min_lines` and
        :attr:`flet.TextField.max_lines` must effectively remain unset.
    """

    suffix_style: Optional[TextStyle] = None
    """
    The text style to use for :attr:`suffix`.
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
