from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
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
class Checkbox(ConstrainedControl, AdaptiveControl):
    """
    Checkbox allows to select one or more items from a group, or switch between two
    mutually exclusive options (checked or unchecked, on or off).
    """

    label: Optional[StrOrControl] = None
    """
    The clickable label to display on the right of a checkbox.
    """

    value: Optional[bool] = False
    """
    The value of this checkbox.

    - If `True` the checkbox is checked.
    - If `False` the checkbox is unchecked.
    - If `None` and [`tristate`][flet.Checkbox.tristate] is `True` the checkbox is indeterminate. (displayed as a dash)
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defines on which side of the checkbox the `label` should be shown.
    """

    label_style: Optional[TextStyle] = None
    """
    The label's style.
    """

    tristate: bool = False
    """
    If `True` the checkbox's [`value`][flet.Checkbox.value] can be `True`, `False`, or `None`.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color that fills the checkbox in
    all or specific [`ControlState`][flet.ControlState]s.

    Supported states: [`ControlState.SELECTED`][flet.ControlState.SELECTED],
    [`ControlState.HOVERED`][flet.ControlState.HOVERED],
    [`ControlState.DISABLED`][flet.ControlState.DISABLED],
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED],
    and [`ControlState.DEFAULT`][flet.ControlState.DEFAULT].
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color of the checkbox's overlay in
    various [`ControlState`][flet.ControlState] states.

    This property supports the following `ControlState` values: `PRESSED`, `SELECTED`,
    `HOVERED` and `FOCUSED`.
    """

    check_color: Optional[ColorValue] = None
    """
    The color to use for the check icon when
    this checkbox is checked.
    """

    active_color: Optional[ColorValue] = None
    """
    The color to use when this checkbox is
    checked.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color to use when this checkbox is
    hovered.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color for the checkbox's Material when it has the input focus.
    If [`overlay_color`][flet.Checkbox.overlay_color] returns a non-None color in the
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED] state, it will be used instead.

    Defaults to [`CheckboxTheme.overlay_color`][flet.CheckboxTheme.overlay_color] in the
    [`FOCUSED`][flet.ControlState.FOCUSED] state, or if that is `None`,
    falls back to [`Theme.focus_color`][flet.Theme.focus_color].
    """

    semantics_label: Optional[str] = None
    """
    The semantic label for the checkbox that is not shown in the UI, but will be
    announced by screen readers in accessibility modes (e.g TalkBack/VoiceOver).
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the checkbox.

    Defaults to [`CheckboxTheme.shape`][flet.CheckboxTheme.shape], or if that is `None`,
    falls back to `RoundedRectangleBorder(radius=2)`.
    """

    splash_radius: Optional[Number] = None
    """
    The radius of the circular Material ink response (ripple) in logical pixels.

    Defaults to [`CheckboxTheme.splash_radius`][flet.CheckboxTheme.splash_radius], or if that is `None`,
    falls back to `20.0`.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    The color and width of the checkbox's border in all or specific [`ControlState`][flet.ControlState]s.

    Supported states: [`ControlState.SELECTED`][flet.ControlState.SELECTED],
    [`ControlState.HOVERED`][flet.ControlState.HOVERED],
    [`ControlState.DISABLED`][flet.ControlState.DISABLED],
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED],
    [`ControlState.PRESSED`][flet.ControlState.PRESSED],
    [`ControlState.ERROR`][flet.ControlState.ERROR],
    and [`ControlState.DEFAULT`][flet.ControlState.DEFAULT].

    Defaults to [`CheckboxTheme.border_side`][flet.CheckboxTheme.border_side], or if that is `None`,
    falls back to `BorderSide` with a width of `2.0`.
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
    The cursor to be displayed when a mouse pointer enters or is hovering over this
    control.

    Defaults to [`CheckboxTheme.mouse_cursor`][flet.CheckboxTheme.mouse_cursor], or if that is `None`,
    falls back to `MouseCursor.CLICK`.
    """

    on_change: Optional[ControlEventHandler["Checkbox"]] = None
    """
    Called when the state of the Checkbox is changed.
    """

    on_focus: Optional[ControlEventHandler["Checkbox"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["Checkbox"]] = None
    """
    Called when the control has lost focus.
    """
