from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    Number,
    StrOrControl,
    VisualDensity,
)

__all__ = ["Checkbox"]


@control("Checkbox")
class Checkbox(LayoutControl, AdaptiveControl):
    """
    Checkbox allows to select one or more items from a group, or switch between two \
    mutually exclusive options (checked or unchecked, on or off).

    ```python
    ft.Checkbox()
    ft.Checkbox(label="Checked", value=True)
    ft.Checkbox(label="Disabled", disabled=True)
    ```
    """

    label: Optional[StrOrControl] = None
    """
    The clickable label to display on the right of a checkbox.
    """

    value: Optional[bool] = False
    """
    The value of this checkbox.

    - If `True`, this checkbox is checked.
    - If `False`, this checkbox is unchecked.
    - If `None` and :attr:`tristate` is `True`, this checkbox
        is indeterminate (displayed as a dash).
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defines on which side of the checkbox the :attr:`label` should be shown.
    """

    label_style: Optional[TextStyle] = None
    """
    The :attr:`label`'s text style.
    """

    tristate: bool = False
    """
    If `True` the checkbox's :attr:`value` can be `True`, `False`, or `None`.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than \
    one control on a page with autofocus set, then the first one added to the page \
    will get focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color that fills this checkbox in all or specific :class:`~flet.ControlState`s.

    Note:
        Supported states: :attr:`flet.ControlState.SELECTED`,
        :attr:`flet.ControlState.HOVERED`, :attr:`flet.ControlState.DISABLED`,
        :attr:`flet.ControlState.FOCUSED`, and :attr:`flet.ControlState.DEFAULT`.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color of this checkbox's overlay in various :class:`~flet.ControlState` states.

    Note:
        Supported states: :attr:`flet.ControlState.PRESSED`,
        :attr:`flet.ControlState.SELECTED`, :attr:`flet.ControlState.HOVERED`,
        :attr:`flet.ControlState.FOCUSED`, and :attr:`flet.ControlState.DEFAULT`.
    """

    check_color: Optional[ColorValue] = None
    """
    The color to use for the check icon when this checkbox is checked.
    """

    active_color: Optional[ColorValue] = None
    """
    The color to use when this checkbox is checked.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color to use when this checkbox is hovered.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color for the checkbox's Material when it has the input focus.
    If :attr:`overlay_color` returns a non-None color in the
    :attr:`flet.ControlState.FOCUSED` state, it will be used instead.

    Defaults to :attr:`flet.CheckboxTheme.overlay_color` in the
    :attr:`flet.ControlState.FOCUSED` state, or if that is `None`,
    falls back to :attr:`flet.Theme.focus_color`.
    """

    semantics_label: Optional[str] = None
    """
    The semantic label for the checkbox that is not shown in the UI, but will be \
    announced by screen readers in accessibility modes (e.g TalkBack/VoiceOver).
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the checkbox.

    Defaults to :attr:`flet.CheckboxTheme.shape`, or if that is `None`,
    falls back to `RoundedRectangleBorder(radius=2)`.
    """

    splash_radius: Optional[Number] = None
    """
    The radius of the circular Material ink response (ripple) in logical pixels.

    Defaults to :attr:`flet.CheckboxTheme.splash_radius`,
    or if that is `None`, falls back to `20.0`.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    The color and width of this checkbox's border in all or specific \
    :class:`~flet.ControlState`s.

    Defaults to :attr:`flet.CheckboxTheme.border_side`, or if that is `None`,
    falls back to `BorderSide` with a width of `2.0`.

    Note:
        Supported states: :attr:`flet.ControlState.SELECTED`,
        :attr:`flet.ControlState.HOVERED`, :attr:`flet.ControlState.DISABLED`,
        :attr:`flet.ControlState.FOCUSED`, :attr:`flet.ControlState.PRESSED`,
        :attr:`flet.ControlState.ERROR`, and :attr:`flet.ControlState.DEFAULT`.
    """

    error: bool = False
    """
    Whether this checkbox wants to show an error state.

    If `True` this checkbox will
    have a different default container color and check color.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the checkbox's layout will be.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this \
    checkbox.

    Defaults to :attr:`flet.CheckboxTheme.mouse_cursor`,
    or if that is `None`, falls back to `MouseCursor.CLICK`.
    """

    on_change: Optional[ControlEventHandler["Checkbox"]] = None
    """
    Called when the state of this checkbox is changed.
    """

    on_focus: Optional[ControlEventHandler["Checkbox"]] = None
    """
    Called when this checkbox has received focus.
    """

    on_blur: Optional[ControlEventHandler["Checkbox"]] = None
    """
    Called when this checkbox has lost focus.
    """
