from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
)

__all__ = ["CupertinoSlidingSegmentedButton"]


@control("CupertinoSlidingSegmentedButton")
class CupertinoSlidingSegmentedButton(LayoutControl):
    """
    A cupertino sliding segmented button.

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

    controls: list[Control]
    """
    The list of segments to be displayed.

    Note:
        Must contain at least two visible Controls.

    Raises:
        ValueError: If it does not contain at least two visible controls.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected segment in the [`controls`][(c).] list.

    Raises:
        IndexError: If it is out of range relative to the visible controls.
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
    The amount of space by which to inset the [`controls`][(c).].
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
    Called when the state of the button is changed -
    when one of the [`controls`][(c).] is clicked.
    """

    def before_update(self):
        super().before_update()
        visible_controls_count = len([c for c in self.controls if c.visible])
        if visible_controls_count < 2:
            raise ValueError(
                f"controls must contain at minimum two visible Controls, "
                f"got {visible_controls_count}"
            )
        if not (0 <= self.selected_index < visible_controls_count):
            raise IndexError(
                f"selected_index ({self.selected_index}) is out of range. "
                f"Expected a value between 0 and {visible_controls_count - 1}, "
                "inclusive."
            )
