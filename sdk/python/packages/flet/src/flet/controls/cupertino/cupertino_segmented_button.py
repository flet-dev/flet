from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import PaddingValue
from flet.controls.types import ColorValue

__all__ = ["CupertinoSegmentedButton"]


@control("CupertinoSegmentedButton")
class CupertinoSegmentedButton(ConstrainedControl):
    """
    An iOS-style segmented button.
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of `Control`s to display as segments inside the CupertinoSegmentedButton.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected segment in the `controls` list.
    """

    selected_color: Optional[ColorValue] = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the button when it is
    selected.
    """

    unselected_color: Optional[ColorValue] = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the button when it is not
    selected.
    """

    border_color: Optional[ColorValue] = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the button's border.
    """

    padding: Optional[PaddingValue] = None
    """
    The button's padding.

    Padding value is an instance of
    [Padding](https://flet.dev/docs/reference/types/padding) class.
    """

    click_color: Optional[ColorValue] = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to fill the background
    of this control when temporarily interacting with through a long press or drag.

    Defaults to the `selected_color` with 20% opacity.
    """

    disabled_color: Optional[ColorValue] = None
    """
    TBD
    """

    disabled_text_color: Optional[ColorValue] = None
    """
    TBD
    """

    on_change: Optional[ControlEventHandler["CupertinoSegmentedButton"]] = None
    """
    Fires when the state of the button is changed - when one of the `controls` is
    clicked.
    """

    def before_update(self):
        super().before_update()
        assert len(self.controls) >= 2, (
            "controls must contain minimum two visible controls"
        )
        if not (0 <= self.selected_index < len(self.controls)):
            raise IndexError(
                f"selected_index {self.selected_index} is out of range. "
                f"Expected a value between 0 and {len(self.controls) - 1}."
            )
