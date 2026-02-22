from typing import Annotated, Optional

from flet.controls._validation import V
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["CupertinoSlider"]


@control("CupertinoSlider")
class CupertinoSlider(LayoutControl):
    """
    An iOS-type slider.

    It provides a visual indication of adjustable content, as well as the current
    setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or
    brightness), or when people would benefit from instant feedback on the effect of
    setting changes.

    Example:
    ```python
    ft.CupertinoSlider(value=0.6)
    ```
    """

    value: Annotated[
        Optional[Number],
        V.ge_field("min"),
        V.le_field("max"),
    ] = None
    """
    The currently selected value for this slider.

    The slider's thumb is drawn at a position that corresponds to this value.

    Raises:
        ValueError: If it is not greater than or equal to [`min`][(c).].
        ValueError: If it is not less than or equal to [`max`][(c).].
    """

    min: Annotated[
        Number,
        V.le_field("max"),
        V.le_field("value"),
    ] = 0.0
    """
    The minimum value the user can select.

    If [`max`][(c).] is equal to the `min`, then this slider is disabled.

    Raises:
        ValueError: If it is not less than or equal to [`max`][(c).].
        ValueError: If it is not less than or equal to [`value`][(c).], when
            [`value`][(c).] is set.
    """

    max: Annotated[
        Number,
        V.ge_field("min"),
        V.ge_field("value"),
    ] = 1.0
    """
    The maximum value the user can select.

    If [`min`][(c).] is equal to the `max`, then this slider is disabled.

    Raises:
        ValueError: If it is not greater than or equal to [`min`][(c).].
        ValueError: If it is not greater than or equal to [`value`][(c).], when
            [`value`][(c).] is set.
    """

    divisions: Optional[int] = None
    """
    The number of discrete divisions.

    If `None`, the slider is continuous.
    """

    active_color: Optional[ColorValue] = None
    """
    The color to use for the portion of the slider track that is active.

    The "active" side of the slider is the side between the thumb and the minimum
    value.
    """

    thumb_color: Optional[ColorValue] = None
    """
    The color of this slider's thumb.
    """

    on_change: Optional[ControlEventHandler["CupertinoSlider"]] = None
    """
    Called when the state of this slider changed.
    """

    on_change_start: Optional[ControlEventHandler["CupertinoSlider"]] = None
    """
    Called when the user starts selecting a new value for this slider.
    """

    on_change_end: Optional[ControlEventHandler["CupertinoSlider"]] = None
    """
    Called when the user is done selecting a new value for this slider.
    """

    on_focus: Optional[ControlEventHandler["CupertinoSlider"]] = None
    """
    Called when this slider has received focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoSlider"]] = None
    """
    Called when this slider has lost focus.
    """

    def before_update(self):
        super().before_update()
        self.value = self.value if self.value is not None else self.min
