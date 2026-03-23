from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    IconData,
    LabelPosition,
    Number,
)

__all__ = ["CupertinoSwitch"]


@control("CupertinoSwitch")
class CupertinoSwitch(LayoutControl):
    """
    An iOS-style switch.

    Used to toggle the on/off state of a single setting.

    Example:
    ```python
           ft.CupertinoSwitch(value=True)
    ```
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
    The position of the :attr:`label` relative to this switch.
    """

    thumb_color: Optional[ColorValue] = None
    """
    The color of this switch's thumb.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for the focus highlight for keyboard interactions.
    """

    autofocus: bool = False
    """
    Whether this switch will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one
    added to the page will get focus.
    """

    on_label_color: Optional[ColorValue] = None
    """
    The color to use for the accessibility label when the switch is on.
    """

    off_label_color: Optional[ColorValue] = None
    """
    The color to use for the accessibility label when the switch is off.
    """

    active_thumb_image_src: Optional[Union[str, bytes]] = None
    """
    An image to use on the thumb of this switch when the switch is on.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.
    """

    inactive_thumb_image_src: Optional[Union[str, bytes]] = None
    """
    An image to use on the thumb of this switch when the switch is off.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.
    """

    active_track_color: Optional[ColorValue] = None
    """
    The color to use on the track when this switch is on.
    """

    inactive_thumb_color: Optional[ColorValue] = None
    """
    The color to use on the thumb when this switch is off.

    If `None`, defaults to :attr:`thumb_color`, and if this is also `None`,
    defaults to :attr:`flet.CupertinoColors.WHITE`.
    """

    inactive_track_color: Optional[ColorValue] = None
    """
    The color to use on the track when this switch is off.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The outline color of this switch's track in various :class:`~flet.ControlState`s.

    Supported states: :attr:`flet.ControlState.SELECTED`,
    :attr:`flet.ControlState.HOVERED`, :attr:`flet.ControlState.DISABLED`,
    :attr:`flet.ControlState.FOCUSED`, and :attr:`flet.ControlState.DEFAULT`.
    """

    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The outline width of this switch's track in all or specific \
    :class:`~flet.ControlState`s.

    Supported states: :attr:`flet.ControlState.SELECTED`,
    :attr:`flet.ControlState.HOVERED`, :attr:`flet.ControlState.DISABLED`,
    :attr:`flet.ControlState.FOCUSED`, and :attr:`flet.ControlState.DEFAULT`.
    """

    thumb_icon: Optional[ControlStateValue[IconData]] = None
    """
    The icon of this Switch's thumb in various :class:`~flet.ControlState`s.

    Supported states: :attr:`flet.ControlState.SELECTED`,
    :attr:`flet.ControlState.HOVERED`, :attr:`flet.ControlState.DISABLED`,
    :attr:`flet.ControlState.FOCUSED`, and :attr:`flet.ControlState.DEFAULT`.
    """

    on_change: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when the state of this switch is changed.
    """

    on_focus: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when this switch has received focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when this switch has lost focus.
    """

    on_image_error: Optional[ControlEventHandler["CupertinoSwitch"]] = None
    """
    Called when :attr:`active_thumb_image_src` or :attr:`inactive_thumb_image_src` \
    fails to load.
    """
