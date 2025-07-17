from dataclasses import field
from enum import Enum
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import Duration, DurationValue
from flet.controls.margin import MarginValue
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    Number,
    StrOrControl,
)

__all__ = ["SnackBar", "SnackBarBehavior", "DismissDirection", "SnackBarAction"]


class SnackBarBehavior(Enum):
    FIXED = "fixed"
    FLOATING = "floating"


class DismissDirection(Enum):
    NONE = "none"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    END_TO_START = "endToStart"
    START_TO_END = "startToEnd"
    UP = "up"
    DOWN = "down"


@control("SnackBar")
class SnackBarAction(Control):
    """
    A button that can be used as an action in a [`SnackBar`][flet.SnackBar].

    An action button for a [`SnackBar`][flet.SnackBar].

    Note:
        - Snack bar actions are always enabled. Instead of disabling a snack bar
            action, avoid including it in the snack bar in the first place.
        -  Snack bar actions can will only respond to first click. Subsequent clicks/presses are ignored.
    """

    label: str
    """
    The button's label.
    """

    text_color: Optional[ColorValue] = None
    """
    The button label color.
    
    If `None`, [`SnackBarTheme.action_text_color`][flet.SnackBarTheme.action_text_color] is used.
    """

    disabled_text_color: Optional[ColorValue] = None
    """
    The button disabled label color.
    This color is shown after the action is dismissed.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The button background fill color.
    
    If `None`, [`SnackBarTheme.action_bgcolor`][flet.SnackBarTheme.action_bgcolor] is used.
    """

    disabled_bgcolor: Optional[ColorValue] = None
    """
    The button disabled background color.
    This color is shown after the action is dismissed.

    If `None`, [`SnackBarTheme.disabled_action_bgcolor`][flet.SnackBarTheme.disabled_action_bgcolor] is used.
    """

    on_click: Optional[ControlEventHandler["SnackBarAction"]] = None
    """
    Called when this action button is clicked.
    """


@control("SnackBar")
class SnackBar(DialogControl):
    """
    A lightweight message with an optional action which briefly displays at the
    bottom of the screen.
    """

    content: StrOrControl
    """
    The primary content of the snack bar.

    Typically a [`Text`][flet.Text] control.
    """

    behavior: Optional[SnackBarBehavior] = None
    """
    This defines the behavior and location of the snack bar.

    Defines where a SnackBar should appear within a page and how its location
    should be adjusted when the page also includes a [`FloatingActionButton`][flet.FloatingActionButton] or a
    [`NavigationBar`][flet.NavigationBar].

    If `None`, [`SnackBarTheme.behavior`][flet.SnackBarTheme.behavior] is used.
    If that's is also `None`, defaults to [`SnackBarBehavior.FIXED`][flet.SnackBarBehavior.FIXED].

    Note:
        - If [`behavior`][flet.SnackBar.behavior] is [`SnackBarBehavior.FLOATING`][flet.SnackBarBehavior.FLOATING], 
          the length of the bar is defined by either [`width`][flet.SnackBar.width] and 
          [`margin`][flet.SnackBar.margin], and if both are specified, `width` takes precedence over `margin`.
        - [`width`][flet.SnackBar.width] and [`margin`][flet.SnackBar.margin] 
          are ignored if `behavior!=SnackBarBehavior.FLOATING`.
    """

    dismiss_direction: Optional[DismissDirection] = None
    """
    The direction in which the SnackBar can be dismissed.

    If `None`, [`SnackBarTheme.dismiss_direction`][flet.SnackBarTheme.dismiss_direction] is used.
    If that's is also `None`, defaults to [`DismissDirection.DOWN`][flet.DismissDirection.DOWN].
    """

    show_close_icon: bool = False
    """
    Whether to include a "close" icon widget.

    Tapping the icon will close the snack bar.
    """

    action: Union[str, SnackBarAction, None] = None
    """
    An optional action that the user can take based on the snack bar.

    For example, the snack bar might let the user undo the operation that prompted
    the snackbar. Snack bars can have at most one action.

    The action should not be "dismiss" or "cancel".
    """

    close_icon_color: Optional[ColorValue] = None
    """
    The color of the close icon, if [`show_close_icon`][flet.SnackBar.show_close_icon] is `True`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    SnackBar background color.
    """

    duration: DurationValue = field(default_factory=lambda: Duration(milliseconds=4000))
    """
    The amount of time this snack bar should stay open for.
    """

    margin: Optional[MarginValue] = None
    """
    Empty space to surround the snack bar.

    Has effect only when `behavior=SnackBarBehavior.FLOATING` and will be ignored
    if `width` is specified.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of padding to apply to the snack bar's content and optional action.
    """

    width: Optional[Number] = None
    """
    The width of the snack bar.

    If width is specified, the snack bar will be centered horizontally in the
    available space.

    Note:
        Has effect only when [`behavior`][flet.SnackBar.behavior] is [`SnackBarBehavior.FLOATING`][flet.SnackBarBehavior.FLOATING]. 
        It can not be used if `margin` is specified.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate at which to place the snack bar. This controls the size of the
    shadow below the snack bar.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this snack bar.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The [`content`][flet.SnackBar.content] will be clipped (or not) according to this option.
    """

    action_overflow_threshold: Number = 0.25
    """
    The percentage threshold for [`action`][flet.SnackBar.action]'s width before
    it overflows to a new line.

    If the width of the snackbar's [`content`][flet.SnackBar.content] is greater than this percentage of the
    width of the snackbar minus the width of its `action`, then the `action` will
    appear below the `content`.

    At a value of `0.0`, the `action` will not overflow to a new line.
    
    Note:
        Must be between `0.0` and `1.0` inclusive.
    """

    on_action: Optional[ControlEventHandler["SnackBar"]] = None
    """
    Called when action button is clicked.
    """

    on_visible: Optional[ControlEventHandler["SnackBar"]] = None
    """
    Called the first time that the snackbar is visible within the page.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or (
            isinstance(self.content, Control) and self.content.visible
        ), "content must be a string or a visible control"
        assert (
            self.action_overflow_threshold is None
            or 0 <= self.action_overflow_threshold <= 1
        ), "action_overflow_threshold must be between 0 and 1 inclusive"
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
