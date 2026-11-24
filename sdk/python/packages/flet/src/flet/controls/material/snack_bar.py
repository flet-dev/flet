from dataclasses import field
from enum import Enum
from typing import Annotated, Optional, Union

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
from flet.utils.validation import V

__all__ = ["DismissDirection", "SnackBar", "SnackBarAction", "SnackBarBehavior"]


class SnackBarBehavior(Enum):
    """
    Defines where a :class:`~flet.SnackBar` appears within a page and how it is \
    positioned relative to bottom UI elements.
    """

    FIXED = "fixed"
    """
    Anchors the snack bar to the bottom of the page.

    If a :class:`~flet.NavigationBar` is present, the snack bar is shown above it.
    Other non-fixed content can be pushed upward while the snack bar is visible.
    """

    FLOATING = "floating"
    """
    Displays the snack bar as a floating surface above page content.

    This mode can overlay bottom widgets, such as a :class:`~flet.NavigationBar` and a
    bottom-positioned :class:`~flet.FloatingActionButton`.
    """


class DismissDirection(Enum):
    """
    Defines swipe directions allowed for dismissing a :class:`~flet.SnackBar`.

    The direction controls which drag gestures can close the snack bar when
    dismissal is enabled.
    """

    NONE = "none"
    """
    Disables swipe-to-dismiss gestures.
    """

    VERTICAL = "vertical"
    """
    Allows dismissing by swiping vertically.

    Users can drag either up or down to dismiss.
    """

    HORIZONTAL = "horizontal"
    """
    Allows dismissing by swiping horizontally.

    Users can drag either left or right to dismiss.
    """

    END_TO_START = "endToStart"
    """
    Allows dismissing toward the end-to-start reading direction.

    For left-to-right locales this is right-to-left; for right-to-left locales
    this is left-to-right.
    """

    START_TO_END = "startToEnd"
    """
    Allows dismissing toward the start-to-end reading direction.

    For left-to-right locales this is left-to-right; for right-to-left locales
    this is right-to-left.
    """

    UP = "up"
    """
    Allows dismissing only by swiping upward.
    """

    DOWN = "down"
    """
    Allows dismissing only by swiping downward.
    """


@control("SnackBar")
class SnackBarAction(Control):
    """
    A button that can be used as an action in a :class:`~flet.SnackBar`.

    An action button for a :class:`~flet.SnackBar`.

    Note:
        - Snack bar actions are always enabled. Instead of disabling a snack bar
            action, avoid including it in the snack bar in the first place.
        - Snack bar actions will only respond to first click.
            Subsequent clicks/presses are ignored.
    """

    label: str
    """
    The button's label.
    """

    text_color: Optional[ColorValue] = None
    """
    The button label color.

    If `None`, :attr:`flet.SnackBarTheme.action_text_color` is used.
    """

    disabled_text_color: Optional[ColorValue] = None
    """
    The button disabled label color.
    This color is shown after the action is dismissed.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The button background fill color.

    If `None`, :attr:`flet.SnackBarTheme.action_bgcolor` is used.
    """

    disabled_bgcolor: Optional[ColorValue] = None
    """
    The button disabled background color.
    This color is shown after the action is dismissed.

    If `None`, :attr:`flet.SnackBarTheme.disabled_action_bgcolor` is used.
    """

    on_click: Optional[ControlEventHandler["SnackBarAction"]] = None
    """
    Called when this action button is clicked.
    """


@control("SnackBar")
class SnackBar(DialogControl):
    """
    A lightweight message with an optional action which briefly displays at the bottom \
    of the screen.

    Example:
    ```python
    page.show_dialog(ft.SnackBar(ft.Text("Opened snack bar")))
    ```
    """

    content: Annotated[
        StrOrControl,
        V.str_or_visible_control(),
    ]
    """
    The primary content of the snack bar.

    Typically a :class:`~flet.Text` control.

    Raises:
        ValueError: If it is neither a string nor a visible `Control`.
    """

    behavior: Optional[SnackBarBehavior] = None
    """
    This defines the behavior and location of the snack bar.

    Defines where a SnackBar should appear within a page and how its location
    should be adjusted when the page also includes a :class:`~flet.FloatingActionButton`
    or a :class:`~flet.NavigationBar`.

    If `None`, :attr:`flet.SnackBarTheme.behavior` is used.
    If that's is also `None`, defaults to :attr:`flet.SnackBarBehavior.FIXED`.

    Note:
        - If :attr:`behavior` is :attr:`flet.SnackBarBehavior.FLOATING`, the length of
            the bar is defined by either :attr:`width` and :attr:`margin`, and if
            both are specified, `width` takes precedence over `margin`.
        - :attr:`width` and :attr:`margin` are ignored if :attr:`behavior`
            is not :attr:`flet.SnackBarBehavior.FLOATING`.
    """

    dismiss_direction: Optional[DismissDirection] = None
    """
    The direction in which the SnackBar can be dismissed.

    If `None`, :attr:`flet.SnackBarTheme.dismiss_direction` is used.
    If that's is also `None`, defaults to :attr:`flet.DismissDirection.DOWN`.
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
    The color of the close icon, if :attr:`show_close_icon` is `True`.
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
        Has effect only when :attr:`behavior` is :attr:`flet.SnackBarBehavior.FLOATING`.
        It can not be used if `margin` is specified.
    """

    elevation: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The z-coordinate at which to place the snack bar. This controls the size of the \
    shadow below the snack bar.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this snack bar.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The :attr:`content` will be clipped (or not) according to this option.
    """

    action_overflow_threshold: Annotated[
        Optional[Number],
        V.between(0.0, 1.0),
    ] = 0.25
    """
    The percentage threshold for :attr:`action`'s width before it overflows to a new \
    line.

    If the width of the snackbar's :attr:`content` is greater than this percentage
    of the width of the snackbar minus the width of its `action`, then the `action`
    will appear below the :attr:`content`.

    At a value of `0.0`, the `action` will not overflow to a new line.

    Raises:
        ValueError: If it is not between `0.0` and `1.0`, inclusive.
    """

    persist: Optional[bool] = None
    """
    Whether the snack bar will stay or auto-dismiss after timeout.

    If `True`, the snack bar remains visible even after the timeout,
    until the user taps the action button or the close icon.

    If `False`, the snack bar will be dismissed after the timeout.

    If not provided, but the snackbar :attr:`action` is not null,
    the snackbar will persist as well.
    """

    on_action: Optional[ControlEventHandler["SnackBar"]] = None
    """
    Called when action button is clicked.
    """

    on_visible: Optional[ControlEventHandler["SnackBar"]] = None
    """
    Called the first time that the snackbar is visible within the page.
    """
