from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
    VisualDensity,
)

__all__ = ["Checkbox"]


@control("Checkbox")
class Checkbox(ConstrainedControl, AdaptiveControl):
    """
    Checkbox allows to select one or more items from a group, or switch between two
    mutually exclusive options (checked or unchecked, on or off).

    Online docs: https://flet.dev/docs/controls/checkbox
    """

    label: Optional[StrOrControl] = None
    """
    The clickable label to display on the right of a checkbox.
    """

    value: Optional[bool] = None
    """
    Current value of the checkbox.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defines on which side of the checkbox the `label` should be shown.

    Value is of type [`LabelPosition`](https://flet.dev/docs/reference/types/labelposition) 
    and defaults to `LabelPosition.RIGHT`.
    """

    label_style: Optional[TextStyle] = None
    """
    The label's style. An instance of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    tristate: bool = False
    """
    If `True` the checkboxes value can be `True`, `False`, or `None`.

    Checkbox displays a dash when its value is `None`.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than 
    one control on a page with autofocus set, then the first one added to the page will 
    get focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) that fills the checkbox in 
    various [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the checkbox's overlay in 
    various [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.

    This property supports the following `ControlState` values: `PRESSED`, `SELECTED`, 
    `HOVERED` and `FOCUSED`.
    """

    check_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the check icon when 
    this checkbox is checked.
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use when this checkbox is 
    checked.
    """

    hover_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use when this checkbox is 
    hovered.
    """

    focus_color: OptionalColorValue = None
    """
    TBD
    """

    semantics_label: Optional[str] = None
    """
    The semantic label for the checkbox that is not shown in the UI, but will be 
    announced by screen readers in accessibility modes (e.g TalkBack/VoiceOver).
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the checkbox. The value is an instance of [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder) 
    class.

    Defaults to `RoundedRectangleBorder(radius=2)`.
    """

    splash_radius: OptionalNumber = None
    """
    The radius of the circular Material ink response (ripple) in logical pixels.

    Defaults to `20.0`.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    TBD
    """

    is_error: bool = False
    """
    Whether this checkbox wants to show an error state. When `True` this checkbox will 
    have a different default container color and check color.

    Defaults to `False`.
    """

    visual_density: Optional[VisualDensity] = None
    """
    TBD
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this 
    control.

    Value is of type [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
    """

    on_change: OptionalControlEventHandler["Checkbox"] = None
    """
    Fires when the state of the Checkbox is changed.
    """

    on_focus: OptionalControlEventHandler["Checkbox"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["Checkbox"] = None
    """
    Fires when the control has lost focus.
    """
