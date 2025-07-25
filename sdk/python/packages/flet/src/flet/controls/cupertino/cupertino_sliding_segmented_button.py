from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
)

__all__ = ["CupertinoSlidingSegmentedButton"]


@control("CupertinoSlidingSegmentedButton")
class CupertinoSlidingSegmentedButton(ConstrainedControl):
    """
    A cupertino sliding segmented button.

    Raises:
        AssertionError: If [`controls`][(c).] does not contain at least two visible controls.
        IndexError: If [`selected_index`][flet.CupertinoSlidingSegmentedButton.selected_index] is out of range.
    """

    controls: list[Control]
    """
    The list of segments to be displayed.

    Note:
        Must contain at least two visible Controls.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected segment in the `controls` list.
    """

    bgcolor: ColorValue = CupertinoColors.TERTIARY_SYSTEM_FILL
    """
    The background color of the button.
    """

    thumb_color: Optional[ColorValue] = None
    """
    The color of the button when it is not
    selected.
    """

    padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(vertical=2, horizontal=3)
    )
    """
    The amount of space by which to inset the [`controls`][flet.CupertinoSlidingSegmentedButton.controls].
    """

    proportional_width: bool = False
    """
    Determine whether segments have proportional widths based on their content.

    If false, all segments will have the same width, determined by the longest
    segment. If true, each segment's width will be determined by its individual
    content.

    If the max width of parent constraints is smaller than the width that the
    segmented control needs, The segment widths will scale down proportionally
    to ensure the segment control fits within the boundaries; similarly, if
    the min width of parent constraints is larger, the segment width will scales
    up to meet the min width requirement.
    """

    on_change: Optional[ControlEventHandler["CupertinoSlidingSegmentedButton"]] = None
    """
    Called when the state of the button is changed - when one of the `controls` is
    clicked.
    """

    def before_update(self):
        super().before_update()
        visible_controls_count = len([c for c in self.controls if c.visible])
        assert visible_controls_count >= 2, (
            f"controls must contain at minimum two visible Controls, "
            f"got {visible_controls_count}"
        )
        if not (0 <= self.selected_index < visible_controls_count):
            raise IndexError(
                f"selected_index ({self.selected_index}) is out of range. "
                f"Expected a value between 0 and {visible_controls_count - 1}, inclusive."
            )
