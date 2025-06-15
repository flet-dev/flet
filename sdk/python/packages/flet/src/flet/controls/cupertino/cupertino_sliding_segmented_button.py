from dataclasses import field

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
    OptionalColorValue,
)

__all__ = ["CupertinoSlidingSegmentedButton"]


@control("CupertinoSlidingSegmentedButton")
class CupertinoSlidingSegmentedButton(ConstrainedControl):
    """
    A CupertinoSlidingSegmentedButton.

    Online docs: https://flet.dev/docs/controls/cupertinoslidingsegmentedbutton
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of `Control`s to display as segments inside the CupertinoSegmentedButton.
    Must have at least 2 items.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected segment in the `controls` list.
    """

    bgcolor: ColorValue = CupertinoColors.TERTIARY_SYSTEM_FILL
    """
    The background [color](https://flet.dev/docs/reference/colors) of the button.
    """

    thumb_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the button when it is not
    selected.
    """

    padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(vertical=2, horizontal=3)
    )
    """
    The button's padding.

    Padding value is an instance of
    [Padding](https://flet.dev/docs/reference/types/padding) class.
    """

    proportional_width: bool = False
    """
    TBD
    """

    on_change: OptionalControlEventHandler["CupertinoSlidingSegmentedButton"] = None
    """
    Fires when the state of the button is changed - when one of the `controls` is 
    clicked.
    """

    def before_update(self):
        super().before_update()
        assert sum(c.visible for c in self.controls) >= 2, (
            "controls must have at minimum two visible Controls"
        )
