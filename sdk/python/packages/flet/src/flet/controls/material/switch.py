from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconData,
    LabelPosition,
    MouseCursor,
    Number,
    StrOrControl,
)

__all__ = ["Switch"]


@control("Switch")
class Switch(LayoutControl, AdaptiveControl):
    """
    A toggle represents a physical switch that allows someone to choose between
    two mutually exclusive options.

    For example, "On/Off", "Show/Hide".

    ```python
        ft.Switch(label="Unchecked switch", value=False)
        ft.Switch(label="Disabled switch", disabled=True)
    ```
    """

    label: Optional[StrOrControl] = None
    """
    The clickable label to display on the right of this switch.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    The position of the [`label`][(c).], if provided.
    """

    label_text_style: Optional[TextStyle] = None
    """
    The [`label`][(c).]'s text style, when it is a string.
    """

    value: bool = False
    """
    Current value of this switch.
    """

    autofocus: bool = False
    """
    Whether this switch will be selected as the initial focus. If there is more
    than one control on a page with autofocus set, then the first one added to
    the page will get focus.
    """

    active_color: Optional[ColorValue] = None
    """
    The color to use when this switch
    is on.
    """

    active_track_color: Optional[ColorValue] = None
    """
    The color to use on the track when
    this switch is on.

    If [`track_color`][(c).] returns a non-none color in
    the `ControlState.SELECTED` state, it will
    be used instead of this color.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for the focus
    highlight for keyboard interactions.
    """

    inactive_thumb_color: Optional[ColorValue] = None
    """
    The color to use on the thumb when
    this switch is off.

    Defaults to colors defined in the
    [material design specification](https://m3.material.io/components/switch/specs).

    If [`thumb_color`][(c).] returns a non-none color
    in the `ControlState.DEFAULT` state, it will be
    used instead of this color.
    """

    inactive_track_color: Optional[ColorValue] = None
    """
    The color to use on the track when
    this switch is off.

    Defaults to colors defined in the
    [material design specification](https://m3.material.io/components/switch/specs).

    If [`track_color`][(c).] returns a non-none color
    in the `ControlState.DEFAULT` state, it will be
    used instead of this color.
    """

    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color of this switch's thumb
    in various [`ControlState`][flet.]
    states.

    The following states are supported: `ControlState.SELECTED`, `ControlState.HOVERED`,
    `ControlState.DISABLED`, `ControlState.FOCUSED` and
    `ControlState.DEFAULT` (fallback).
    """

    thumb_icon: Optional[ControlStateValue[IconData]] = None
    """
    The icon of this Switch's thumb in various
    [`ControlState`][flet.] states.

    The following states are supported: `ControlState.SELECTED`, `ControlState.HOVERED`,
    `ControlState.DISABLED`, `ControlState.FOCUSED` and
    `ControlState.DEFAULT` (fallback).
    """

    track_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color of this switch's track
    in various [`ControlState`][flet.]  states.

    The following states are supported: `ControlState.SELECTED`,
    `ControlState.HOVERED`, `ControlState.DISABLED`, `ControlState.FOCUSED` and
    `ControlState.DEFAULT` (fallback).
    """

    adaptive: Optional[bool] = None
    """
    Whether an adaptive Switch should be created based on the target platform.

    On iOS and macOS, a [`CupertinoSwitch`][flet.] is created,
    which has matching functionality and presentation as `Switch`,
    and the graphics as expected on iOS. On other platforms,
    a Material Switch is created.

    Defaults to `False`. See the example of usage
    [here](https://flet.dev/docs/controls/cupertinoswitch#cupertinoswitch-and-adaptive-switch).
    """

    hover_color: Optional[ColorValue] = None
    """
    The color to be used when it is
    being hovered over by the mouse pointer.
    """

    splash_radius: Optional[Number] = None
    """
    The radius of the splash effect when the switch is pressed.

    Raises:
        ValueError: If [`splash_radius`][(c).] is negative.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color for the switch's
    Material in various
    [`ControlState`][flet.] states.

    The following states are supported: `ControlState.PRESSED`,
    `ControlState.SELECTED`, `ControlState.HOVERED`, `ControlState.FOCUSED` and
    `ControlState.DEFAULT`.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The outline color of this switch's
    track in various [`ControlState`][flet.]
    states.

    The following states are supported: `ControlState.SELECTED`, `
    ControlState.HOVERED`, `ControlState.DISABLED`, `ControlState.FOCUSED` and
    `ControlState.DEFAULT` (fallback).
    """

    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The outline width of this switch's track in all or specific
    [`ControlState`][flet.] states.

    The following states are supported: `ControlState.SELECTED`,
    `ControlState.HOVERED`, `ControlState.DISABLED`,
    `ControlState.FOCUSED` and `ControlState.DEFAULT` (fallback).
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over
    this control.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space to surround the child inside the bounds of the Switch.

    Defaults to horizontal padding of 4 pixels. If
    [`Theme.use_material3`][flet.] is false, then there is no
    padding by default.
    """

    on_change: Optional[ControlEventHandler["Switch"]] = None
    """
    Called when the state of the Switch is changed.
    """

    on_focus: Optional[ControlEventHandler["Switch"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["Switch"]] = None
    """
    Called when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        if self.splash_radius is not None and self.splash_radius < 0:
            raise ValueError(
                "splash_radius must be greater than or equal to 0, "
                f"got {self.splash_radius}"
            )
