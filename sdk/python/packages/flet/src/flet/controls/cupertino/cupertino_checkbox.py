from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
)

__all__ = ["CupertinoCheckbox"]


@control("CupertinoCheckbox")
class CupertinoCheckbox(ConstrainedControl):
    """
    A macOS style checkbox. Checkbox allows to select one or more items from a group,
    or switch between two mutually exclusive options (checked or unchecked, on or off).

    Online docs: https://flet.dev/docs/controls/cupertinocheckbox
    """

    label: Optional[str] = None
    """
    The clickable label to display on the right of a checkbox.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defines on which side of the checkbox the `label` should be shown.

    Value is of type [`LabelPosition`](https://flet.dev/docs/reference/types/labelposition) 
    and defaults to `RIGHT`.
    """

    value: Optional[bool] = None
    """
    Current value of the checkbox.
    """

    tristate: bool = True
    """
    If `True` the checkbox's value can be `True`, `False`, or `None`.

    Checkbox displays a dash when its value is null.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than 
    one control on a page with autofocus set, then the first one added to the page will 
    get focus.
    """

    check_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the check icon when 
    this checkbox is checked.
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to fill checkbox when it 
    is checked/selected.

    If `fill_color` returns a non-null color in the `SELECTED` state, it will be used 
    instead of this color.

    Defaults to `Colors.PRIMARY`.
    """

    focus_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used for the checkbox's border 
    shadow when it has the input focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to fill the checkbox in 
    all or specific [`ControlState`](https://flet.dev/docs/reference/types/controlstate) 
    states.

    The following states are supported: `DEFAULT`, `SELECTED`, `HOVERED`, `FOCUSED`, 
    and `DISABLED`.

    `active_color` is used as fallback color when the checkbox is in the `SELECTED` 
    state, `CupertinoColors.WHITE` at 50% opacity is used as fallback color when the 
    checkbox is in the `DISABLED` state, and `CupertinoColors.WHITE` otherwise.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the checkbox.

    Value is of type [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder) 
    and defaults to `RoundedRectangleBorder(radius=4)`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer entering or hovering over this control.

    Value is of type [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
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
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.

    The following states are supported: `DEFAULT`, `PRESSED`, `SELECTED`, `HOVERED`, 
    `FOCUSED`, `DISABLED` and `ERROR`.
    """

    on_change: OptionalControlEventHandler["CupertinoCheckbox"] = None
    """
    Fires when the state of the Checkbox is changed.
    """

    on_focus: OptionalControlEventHandler["CupertinoCheckbox"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["CupertinoCheckbox"] = None
    """
    Fires when the control has lost focus.
    """
