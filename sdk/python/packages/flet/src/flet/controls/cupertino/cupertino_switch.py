from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.types import (
    ColorValue,
    IconValue,
    LabelPosition,
    OptionalColorValue,
    OptionalNumber,
)

__all__ = ["CupertinoSwitch"]


@control("CupertinoSwitch")
class CupertinoSwitch(ConstrainedControl):
    """
    An iOS-style switch. Used to toggle the on/off state of a single setting.

    Online docs: https://flet.dev/docs/controls/cupertinoswitch
    """

    label: Optional[str] = None
    """
    The clickable label to display on the right of the switch.
    """

    value: bool = False
    """
    Current value of the switch.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    The position of the label relative to the switch.

    Value is of type 
    [LabelPosition](https://flet.dev/docs/reference/types/labelposition) and defaults 
    to `LabelPosition.RIGHT`.
    """

    thumb_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the switch's thumb.
    """

    focus_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the focus highlight 
    for keyboard interactions.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one 
    added to the page will get focus.
    """

    on_label_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the accessibility 
    label when the switch is on.
    """

    off_label_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the accessibility 
    label when the switch is off.
    """

    active_thumb_image: Optional[str] = None
    """
    An image to use on the thumb of this switch when the switch is on.

    Can be a local file path or URL.
    """

    inactive_thumb_image: Optional[str] = None
    """
    An image to use on the thumb of this switch when the switch is off.

    Can be a local file path or URL.
    """

    active_track_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use on the track when this 
    switch is on.
    """

    inactive_thumb_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use on the thumb when this 
    switch is off.

    If `None`, defaults to `thumb_color`, or `CupertinoColors.WHITE` if `thumb_color` 
    is also `None`.
    """

    inactive_track_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use on the track when this 
    switch is off.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The outline [color](https://flet.dev/docs/reference/colors) of this switch's track 
    in various 
    [ControlState](https://flet.dev/docs/reference/types/controlstate) states.
    """

    track_outline_width: Optional[ControlStateValue[OptionalNumber]] = None
    """
    The outline width of this switch's track in all or specific 
    [ControlState](https://flet.dev/docs/reference/types/controlstate) states.
    """

    thumb_icon: Optional[ControlStateValue[IconValue]] = None
    """
    The icon of this Switch's thumb in various 
    [ControlState](https://flet.dev/docs/reference/types/controlstate) states.

    Supported values: `SELECTED`, `HOVERED`, `DISABLED`, `FOCUSED`, `DEFAULT`.
    """

    on_change: OptionalControlEventHandler["CupertinoSwitch"] = None
    """
    Fires when the state of the switch is changed.
    """

    on_focus: OptionalControlEventHandler["CupertinoSwitch"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["CupertinoSwitch"] = None
    """
    Fires when the control has lost focus.
    """

    on_image_error: OptionalControlEventHandler["CupertinoSwitch"] = None
    """
    Fires when the image (`active_thumb_image` or `inactive_thumb_image`) fails to 
    load.
    """
