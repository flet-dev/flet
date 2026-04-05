from dataclasses import field
from typing import Annotated, Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
)
from flet.utils.validation import V

__all__ = ["CupertinoSlidingSegmentedButton"]


@control("CupertinoSlidingSegmentedButton")
class CupertinoSlidingSegmentedButton(LayoutControl):
    """
    A cupertino sliding segmented button.

    Example:
    ```python
    ft.CupertinoSlidingSegmentedButton(
        selected_index=1,
        controls=[
            ft.Text("One"),
            ft.Text("Two"),
            ft.Text("Three"),
        ],
    )
    ```
    """

    controls: Annotated[
        list[Control],
        V.visible_controls(min_count=2),
    ]
    """
    The list of segments to be displayed.

    Raises:
        ValueError: If it does not contain at least two visible `Control`s.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected segment in the :attr:`controls` list.

    Raises:
        IndexError: If it is not between `0` and the length of visible
            :attr:`controls`, inclusive.
    """

    bgcolor: ColorValue = CupertinoColors.TERTIARY_SYSTEM_FILL
    """
    The background color of this button.
    """

    thumb_color: Optional[ColorValue] = None
    """
    The color of this button when it is not selected.
    """

    padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(vertical=2, horizontal=3)
    )
    """
    The amount of space by which to inset the :attr:`controls`.
    """

    proportional_width: bool = False
    """
    Determine whether segments have proportional widths based on their content.

    If `False`, all segments will have the same width, determined by the longest
    segment. If `True`, each segment's width will be determined by its individual
    content.

    If the max width of parent constraints is smaller than the width that this control
    needs, the segment widths will scale down proportionally to ensure this control
    fits within the boundaries; similarly, if the min width of parent constraints is
    larger, the segment width will scales up to meet the min width requirement.
    """

    on_change: Optional[ControlEventHandler["CupertinoSlidingSegmentedButton"]] = None
    """
    Called when the state of the button is changed - when one of the :attr:`controls` \
    is clicked.
    """

    def before_update(self):
        super().before_update()
        visible_controls_count = len([c for c in self.controls if c.visible])
        if visible_controls_count >= 2 and not (
            0 <= self.selected_index < visible_controls_count
        ):
            raise IndexError(
                f"selected_index ({self.selected_index}) is out of range. "
                f"Expected a value between 0 and {visible_controls_count - 1}, "
                "inclusive."
            )
