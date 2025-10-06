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
    Checkbox allows to select one or more items from a group, or switch between two
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
    - If `None` and [`tristate`][(c).] is `True`, this checkbox
        is indeterminate (displayed as a dash).
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defines on which side of the checkbox the [`label`][(c).] should be shown.
    """

    label_style: Optional[TextStyle] = None
    """
    The [`label`][(c).]'s text style.
    """

    tristate: bool = False
    """
    If `True` the checkbox's [`value`][(c).] can be `True`, `False`, or `None`.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color that fills this checkbox in all or specific [`ControlState`][flet.]s.

    Note:
        Supported states: [`ControlState.SELECTED`][flet.],
        [`ControlState.HOVERED`][flet.], [`ControlState.DISABLED`][flet.],
        [`ControlState.FOCUSED`][flet.], and [`ControlState.DEFAULT`][flet.].
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color of this checkbox's overlay in various [`ControlState`][flet.] states.

    Note:
        Supported states: [`ControlState.PRESSED`][flet.],
        [`ControlState.SELECTED`][flet.], [`ControlState.HOVERED`][flet.],
        [`ControlState.FOCUSED`][flet.], and [`ControlState.DEFAULT`][flet.].
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
    If [`overlay_color`][(c).] returns a non-None color in the
    [`ControlState.FOCUSED`][flet.] state, it will be used instead.

    Defaults to [`CheckboxTheme.overlay_color`][flet.] in the
    [`ControlState.FOCUSED`][flet.] state, or if that is `None`,
    falls back to [`Theme.focus_color`][flet.].
    """

    semantics_label: Optional[str] = None
    """
    The semantic label for the checkbox that is not shown in the UI, but will be
    announced by screen readers in accessibility modes (e.g TalkBack/VoiceOver).
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the checkbox.

    Defaults to [`CheckboxTheme.shape`][flet.], or if that is `None`,
    falls back to `RoundedRectangleBorder(radius=2)`.
    """

    splash_radius: Optional[Number] = None
    """
    The radius of the circular Material ink response (ripple) in logical pixels.

    Defaults to [`CheckboxTheme.splash_radius`][flet.],
    or if that is `None`, falls back to `20.0`.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    The color and width of this checkbox's border in all or specific
    [`ControlState`][flet.]s.

    Defaults to [`CheckboxTheme.border_side`][flet.], or if that is `None`,
    falls back to `BorderSide` with a width of `2.0`.

    Note:
        Supported states: [`ControlState.SELECTED`][flet.],
        [`ControlState.HOVERED`][flet.], [`ControlState.DISABLED`][flet.],
        [`ControlState.FOCUSED`][flet.], [`ControlState.PRESSED`][flet.],
        [`ControlState.ERROR`][flet.], and [`ControlState.DEFAULT`][flet.].
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
    checkbox.

    Defaults to [`CheckboxTheme.mouse_cursor`][flet.],
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
