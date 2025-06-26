from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconValue,
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
)

__all__ = ["Switch"]


@control("Switch")
class Switch(ConstrainedControl, AdaptiveControl):
    """
    A toggle represents a physical switch that allows someone to choose between
    two mutually exclusive options.

    For example, "On/Off", "Show/Hide". Choosing an option should produce
    an immediate result.

    Online docs: https://flet.dev/docs/controls/switch
    """

    label: Optional[StrOrControl] = None
    """
    The clickable label to display on the right of the Switch.
    """

    label_position: Optional[LabelPosition] = None
    """
    Value is of type
    [`LabelPosition`](https://flet.dev/docs/reference/types/labelposition) and
    defaults to `LabelPosition.RIGHT`.
    """

    label_style: Optional[TextStyle] = None
    """
    The label's style.

    Value is of type
    [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    value: bool = False
    """
    Current value of the Switch.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more
    than one control on a page with autofocus set, then the first one added to
    the page will get focus.
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use when this switch
    is on.
    """

    active_track_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use on the track when
    this switch is on.

    If `track_color` returns a non-null color in the `SELECTED` state, it will
    be used instead of this color.
    """

    focus_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the focus
    highlight for keyboard interactions.
    """

    inactive_thumb_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use on the thumb when
    this switch is off.

    Defaults to colors defined in the
    [material design specification](https://m3.material.io/components/switch/specs).

    If `thumb_color` returns a non-null color in the `DEFAULT` state, it will be
    used instead of this color.
    """

    inactive_track_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use on the track when
    this switch is off.

    Defaults to colors defined in the
    [material design specification](https://m3.material.io/components/switch/specs).

    If `track_color` returns a non-null color in the `DEFAULT` state, it will be
    used instead of this color.
    """

    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) of this switch's thumb
    in various [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    states.

    The following [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    values are supported: `SELECTED`, `HOVERED`, `DISABLED`, `FOCUSED` and
    `DEFAULT` (fallback).
    """

    thumb_icon: Optional[ControlStateValue[IconValue]] = None
    """
    The icon of this Switch's thumb in various
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.

    The following [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    values are supported: `SELECTED`, `HOVERED`, `DISABLED`, `FOCUSED` and
    `DEFAULT` (fallback).
    """

    track_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) of this switch's track
    in various [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    states.

    The following [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    values are supported: `SELECTED`, `HOVERED`, `DISABLED`, `FOCUSED` and
    `DEFAULT` (fallback).
    """

    adaptive: Optional[bool] = None
    """
    If the value is `True`, an adaptive Switch is created based on whether the
    target platform is iOS/macOS.

    On iOS and macOS, a `CupertinoSwitch` is created, which has matching
    functionality and presentation as `Switch`, and the graphics as expected on
    iOS. On other platforms, a Material Switch is created.

    Defaults to `False`. See the example of usage
    [here](https://flet.dev/docs/controls/cupertinoswitch#cupertinoswitch-and-adaptive-switch).
    """

    hover_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to be used when it is
    being hovered over by the mouse pointer.
    """

    splash_radius: OptionalNumber = None
    """
    The radius of the splash effect when the switch is pressed.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) for the switch's
    Material in various
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.

    The following [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    values are supported: `PRESSED`, `SELECTED`, `HOVERED`, `FOCUSED` and
    `DEFAULT`.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The outline [color](https://flet.dev/docs/reference/colors) of this switch's
    track in various [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    states.

    The following [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    values are supported: `SELECTED`, `HOVERED`, `DISABLED`, `FOCUSED` and
    `DEFAULT` (fallback).
    """

    track_outline_width: Optional[ControlStateValue[OptionalNumber]] = None
    """
    The outline width of this switch's track in all or specific
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.

    The following states are supported: `SELECTED`, `HOVERED`, `DISABLED`,
    `FOCUSED` and `DEFAULT` (fallback).
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over
    this control.

    The value is
    [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor) enum.
    """

    on_change: OptionalControlEventHandler["Switch"] = None
    """
    Fires when the state of the Switch is changed.
    """

    on_focus: OptionalControlEventHandler["Switch"] = None
    """
    Fires when the control has received focus.

    Event handler argument is of type
    [`OnFocusEvent`](https://flet.dev/docs/reference/types/onfocusevent).
    """

    on_blur: OptionalControlEventHandler["Switch"] = None
    """
    Fires when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        assert self.splash_radius is None or self.splash_radius >= 0, (
            "splash_radius cannot be negative"
        )
