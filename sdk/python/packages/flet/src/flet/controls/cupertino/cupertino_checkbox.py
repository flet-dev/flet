from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
)

__all__ = ["CupertinoCheckbox"]


@control("CupertinoCheckbox")
class CupertinoCheckbox(LayoutControl):
    """
    A macOS style checkbox. Checkbox allows to select one or more items from a group,
    or switch between two mutually exclusive options (checked or unchecked, on or off).
    """

    label: Optional[str] = None
    """
    The clickable label to display on the right of a checkbox.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defines on which side of the checkbox the [`label`][flet.CupertinoCheckbox.label]
    should be shown.
    """

    value: Optional[bool] = False
    """
    The value of this checkbox.

    - If `True` the checkbox is checked.
    - If `False` the checkbox is unchecked.
    - If `None` and [`tristate`][flet.CupertinoCheckbox.tristate] is `True`
        the checkbox is indeterminate. (displayed as a dash)
    """

    tristate: bool = False
    """
    If `True` the checkbox's [`value`][flet.CupertinoCheckbox.value] can be `True`,
    `False`, or `None`.
    """

    autofocus: bool = False
    """
    Whether this control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    check_color: Optional[ColorValue] = None
    """
    The color to use for the check icon when
    this checkbox is checked.
    """

    active_color: Optional[ColorValue] = CupertinoColors.ACTIVE_BLUE
    """
    The color used to fill checkbox when it
    is checked/selected.

    If [`fill_color`][flet.CupertinoCheckbox.fill_color] returns a non-null color in the
    `ControlState.SELECTED` state, it will be used instead of this color.

    Defaults to `Colors.PRIMARY`.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color used for the checkbox's border
    shadow when it has the input focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color used to fill the checkbox in
    all or specific [`ControlState`][flet.ControlState]
    states.

    Supported states: [`ControlState.SELECTED`][flet.ControlState.SELECTED],
    [`ControlState.HOVERED`][flet.ControlState.HOVERED],
    [`ControlState.DISABLED`][flet.ControlState.DISABLED],
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED],
    and [`ControlState.DEFAULT`][flet.ControlState.DEFAULT].

    [`active_color`][flet.CupertinoCheckbox.active_color] is used as fallback color when
    the checkbox is in the `SELECTED` state, `CupertinoColors.WHITE` at 50% opacity
    is used as fallback color when this checkbox is in the `DISABLED` state,
    and `CupertinoColors.WHITE` otherwise.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this checkbox.

    Internally defaults to `RoundedRectangleBorder(radius=4)`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer entering or hovering over this checkbox.
    """

    semantics_label: Optional[str] = None
    """
    The semantic label for the checkbox that will be announced by screen readers.

    This is announced by assistive technologies (e.g TalkBack/VoiceOver) and not shown
    on the UI.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    Defines the checkbox's border sides in all or specific
    [`ControlState`][flet.ControlState] states.

    Supported states: [`ControlState.SELECTED`][flet.ControlState.SELECTED],
    [`ControlState.HOVERED`][flet.ControlState.HOVERED],
    [`ControlState.DISABLED`][flet.ControlState.DISABLED],
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED],
    [`ControlState.PRESSED`][flet.ControlState.PRESSED],
    [`ControlState.ERROR`][flet.ControlState.ERROR],
    and [`ControlState.DEFAULT`][flet.ControlState.DEFAULT].
    """

    on_change: Optional[ControlEventHandler["CupertinoCheckbox"]] = None
    """
    Called when the state of this checkbox is changed.
    """

    on_focus: Optional[ControlEventHandler["CupertinoCheckbox"]] = None
    """
    Called when this checkbox has received focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoCheckbox"]] = None
    """
    Called when this checkbox has lost focus.
    """
