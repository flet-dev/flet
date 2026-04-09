from typing import Annotated, Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
)
from flet.utils.validation import V

__all__ = ["RangeSlider"]


@control("RangeSlider")
class RangeSlider(LayoutControl):
    """
    A Material Design range slider. Used to select a range from a range of values.

    A range slider can be used to select from either a continuous or a discrete
    set of values. The default is to use a continuous range of values from
    :attr:`min` to :attr:`max`.

    Example:
    ```python
    ft.RangeSlider(
        min=0,
        max=10,
        start_value=2,
        divisions=10,
        end_value=7,
    )
    ```
    """

    start_value: Annotated[
        Number,
        V.ge_field("min"),
        V.le_field("end_value"),
    ]
    """
    The currently selected start value for this slider.

    The left thumb of this slider is drawn at a position that corresponds
    to this value. Use :attr:`label` to change the label displayed on the thumb.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`min`.
        ValueError: If it is not less than or equal to :attr:`end_value`.
    """

    end_value: Annotated[
        Number,
        V.le_field("max"),
        V.ge_field("start_value"),
    ]
    """
    The currently selected end value of this slider.

    The right thumb of this slider is drawn at a position that corresponds
    to this value. Use :attr:`label` to change the label displayed on the thumb.

    Raises:
        ValueError: If it is not less than or equal to :attr:`max`.
        ValueError: If it is not greater than or equal to :attr:`start_value`.
    """

    label: Optional[str] = None
    """
    A label to show above the slider thumbs when the slider is active.

    It may contain `{value}` which will be replaced with realtime values of
    :attr:`start_value` and :attr:`end_value`, in the corresponding slider thumbs.

    If not set, then the labels will not be displayed.
    If :attr:`divisions` is not set, this slider is
    continuous and labels are not displayed.
    """

    min: Annotated[
        Number,
        V.le_field("start_value"),
        V.le_field("max"),
    ] = 0.0
    """
    The minimum value the user can select.

    If the :attr:`max` is equal to the `min`, then the slider is disabled.

    Raises:
        ValueError: If it is not less than or equal to :attr:`start_value`.
        ValueError: If it is not less than or equal to :attr:`max`.
    """

    max: Annotated[
        Number,
        V.ge_field("end_value"),
        V.ge_field("min"),
    ] = 1.0
    """
    The maximum value the user can select.

    If the :attr:`max` is equal to the :attr:`min`, then the slider is disabled.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`end_value`.
        ValueError: If it is not greater than or equal to :attr:`min`.
    """

    divisions: Annotated[
        Optional[int],
        V.gt(0),
    ] = None
    """
    The number of discrete divisions.

    Typically used with :attr:`label` to show the current discrete values.

    If not set, this slider is continuous and :attr:`label` is not displayed.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    round: Annotated[
        int,
        V.between(0, 20),
    ] = 0
    """
    The number of decimals displayed on the :attr:`label` containing `{value}`.

    Defaults to `0` - value rounded to the nearest integer.

    Raises:
        ValueError: If it is not between `0` and `20`, inclusive.
    """

    active_color: Optional[ColorValue] = None
    """
    The color to use for the portion of the slider track that is active.

    The "active" segment of the range slider is the span between the thumbs.
    """

    inactive_color: Optional[ColorValue] = None
    """
    The color for the inactive portions of the slider track.

    The "inactive" segments of the slider are the span of tracks between the min and
    the start thumb, and the end thumb and the max.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight color that's typically used to indicate that the range slider thumb \
    is in :attr:`flet.ControlState.HOVERED` or :attr:`flet.ControlState.DRAGGED` \
    state.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    The cursor for a mouse pointer entering or hovering over this control.
    """

    on_change: Optional[ControlEventHandler["RangeSlider"]] = None
    """
    Called when the state of this slider is changed.
    """

    on_change_start: Optional[ControlEventHandler["RangeSlider"]] = None
    """
    Called when the user starts selecting a new value for this slider.
    """

    on_change_end: Optional[ControlEventHandler["RangeSlider"]] = None
    """
    Called when the user is done selecting a new value for this slider.
    """
