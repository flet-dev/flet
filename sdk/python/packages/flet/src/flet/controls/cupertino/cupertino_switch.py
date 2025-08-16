from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.types import (
    ColorValue,
    IconData,
    LabelPosition,
    Number,
)

__all__ = ["CupertinoSwitch"]


@control("CupertinoSwitch")
class CupertinoSwitch(ConstrainedControl):
    """
    An iOS-style switch. Used to toggle the on/off state of a single setting.
    """

    label: Optional[str] = None
    """
    The clickable label to display on the right of this switch.
    """

    value: bool = False
    """
    The current value of this switch.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    The position of the label relative to the switch.
    """

    thumb_color: Optional[ColorValue] = None
    """
    The color of this switch's thumb.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for the focus highlight
    for keyboard interactions.
    """

    autofocus: bool = False
    """
    Whether this switch will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one
    added to the page will get focus.
    """

    on_label_color: Optional[ColorValue] = None
    """
    The color to use for the accessibility
    label when the switch is on.
    """

    off_label_color: Optional[ColorValue] = None
    """
    The color to use for the accessibility
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

    active_track_color: Optional[ColorValue] = None
    """
    The color to use on the track when this
    switch is on.
    """

    inactive_thumb_color: Optional[ColorValue] = None
    """
    The color to use on the thumb when this
    switch is off.

    If `None`, defaults to [`thumb_color`][flet.CupertinoSwitch.thumb_color],
    and if this is also `None`, defaults to
    [`CupertinoColors.WHITE`][flet.CupertinoColors.WHITE].
    """

    inactive_track_color: Optional[ColorValue] = None
    """
    The color to use on the track when this
    switch is off.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The outline color of this switch's track
    in various [`ControlState`][flet.ControlState]s.

    Supported states: [`ControlState.SELECTED`][flet.ControlState.SELECTED],
    [`ControlState.HOVERED`][flet.ControlState.HOVERED],
    [`ControlState.DISABLED`][flet.ControlState.DISABLED],
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED],
    and [`ControlState.DEFAULT`][flet.ControlState.DEFAULT].
    """

    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The outline width of this switch's track in all or specific
    [`ControlState`][flet.ControlState]s.

    Supported states: [`ControlState.SELECTED`][flet.ControlState.SELECTED],
    [`ControlState.HOVERED`][flet.ControlState.HOVERED],
    [`ControlState.DISABLED`][flet.ControlState.DISABLED],
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED],
    and [`ControlState.DEFAULT`][flet.ControlState.DEFAULT].
    """

    thumb_icon: Optional[ControlStateValue[IconData]] = None
    """
    The icon of this Switch's thumb in various
    [`ControlState`][flet.ControlState]s.

    Supported states: [`ControlState.SELECTED`][flet.ControlState.SELECTED],
    [`ControlState.HOVERED`][flet.ControlState.HOVERED],
    [`ControlState.DISABLED`][flet.ControlState.DISABLED],
    [`ControlState.FOCUSED`][flet.ControlState.FOCUSED],
    and [`ControlState.DEFAULT`][flet.ControlState.DEFAULT].
    """

    on_change: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when the state of the switch is changed.
    """

    on_focus: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when the control has lost focus.
    """

    on_image_error: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when the image ([`active_thumb_image`][flet.CupertinoSwitch.active_thumb_image] or
    [`inactive_thumb_image`][flet.CupertinoSwitch.inactive_thumb_image]) fails to load.
    """  # noqa: E501
