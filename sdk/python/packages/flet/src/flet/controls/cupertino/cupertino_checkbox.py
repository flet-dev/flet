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
    Number,
)

__all__ = ["CupertinoCheckbox"]


@control("CupertinoCheckbox")
class CupertinoCheckbox(LayoutControl):
    """
    A macOS style checkbox.

    Checkbox allows to select one or more items from a group,
    or switch between two mutually exclusive options (checked or unchecked, on or off).

    ```python
    ft.Column(
        intrinsic_width=True,
        controls=[
            ft.CupertinoCheckbox(),
            ft.CupertinoCheckbox(label="Checked", value=True),
            ft.CupertinoCheckbox(label="Disabled", disabled=True),
        ],
    )
    ```
    """

    label: Optional[str] = None
    """
    A clickable label to display on the right of this checkbox.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defines on which side of this checkbox the [`label`][(c).] should be shown.
    """

    spacing: Optional[Number] = 10
    """
    The space between this checkbox and the [`label`][(c).].
    """

    value: Optional[bool] = False
    """
    The value of this checkbox.

    - If `True`, this checkbox is checked.
    - If `False`, this checkbox is unchecked.
    - If `None` and [`tristate`][(c).] is `True`,
        this checkbox is indeterminate (displayed as a dash).
    """

    tristate: bool = False
    """
    If `True`, this checkbox's [`value`][(c).] can be `True`, `False`, or `None`.
    """

    autofocus: bool = False
    """
    Whether this checkbox will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    check_color: Optional[ColorValue] = None
    """
    The color to use for the check icon when this checkbox is checked.
    """

    active_color: Optional[ColorValue] = CupertinoColors.ACTIVE_BLUE
    """
    The color used to fill checkbox when it
    is checked/selected.

    If [`fill_color`][(c).] returns a non-null color in the
    [`ControlState.SELECTED`][flet.] state, it will be used instead of this color.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color used for this checkbox's border shadow when it has the input focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color used to fill this checkbox in all or specific [`ControlState`][flet.]
    states.

    [`active_color`][(c).] is used as fallback color when
    the checkbox is in the [`SELECTED`][flet.ControlState.] state,
    [`CupertinoColors.WHITE`][flet.] at `50%` opacity is used as fallback color
    when this checkbox is in the [`DISABLED`][flet.ControlState.] state, and
    [`CupertinoColors.WHITE`][flet.] otherwise.

    Note:
        Supported states: [`ControlState.SELECTED`][flet.],
        [`ControlState.HOVERED`][flet.], [`ControlState.DISABLED`][flet.],
        [`ControlState.FOCUSED`][flet.], and [`ControlState.DEFAULT`][flet.].
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
    The semantic label for this checkbox that will be announced by screen readers.

    This is announced by assistive technologies (e.g TalkBack/VoiceOver) and not shown
    on the UI.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    Defines the checkbox's border sides in all or specific
    [`ControlState`][flet.] states.

    Note:
        Supported states: [`ControlState.SELECTED`][flet.],
        [`ControlState.HOVERED`][flet.], [`ControlState.DISABLED`][flet.],
        [`ControlState.FOCUSED`][flet.], [`ControlState.PRESSED`][flet.],
        [`ControlState.ERROR`][flet.], and [`ControlState.DEFAULT`][flet.].
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
