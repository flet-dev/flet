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

    Raises:
        AssertionError: If [`controls`][(c).] does not contain at least two visible controls.
        IndexError: If [`selected_index`][flet.CupertinoSegmentedButton.selected_index] is out of range.
    """

    controls: list[Control]
    """
    The list of segments to be displayed.

    Note:
        Must contain at least two visible Controls.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected segment in the
    [`controls`][flet.CupertinoSegmentedButton.controls] list.
    """

    selected_color: Optional[ColorValue] = None
    """
    The color of the button when it is
    selected.
    """

    unselected_color: Optional[ColorValue] = None
    """
    The color of the button when it is not
    selected.
    """

    border_color: Optional[ColorValue] = None
    """
    The color of the button's border.
    """

    padding: Optional[PaddingValue] = None
    """
    The button's padding.
    """

    click_color: Optional[ColorValue] = None
    """
    The color used to fill the background
    of this control when temporarily interacting with through a long press or drag.

    Defaults to the [`selected_color`][flet.CupertinoSegmentedButton.selected_color] with 20% opacity.
    """

    disabled_color: Optional[ColorValue] = None
    """
    The color used to fill the background of the segment when it is disabled.

    If `None`, this color will be 50% opacity of the [`selected_color`][flet.CupertinoSegmentedButton.selected_color] when
    the segment is selected. If the segment is unselected, this color will be
    set to the [`unselected_color`][flet.CupertinoSegmentedButton.unselected_color].
    """

    disabled_text_color: Optional[ColorValue] = None
    """
    The color used for the text of the segment when it is disabled.
    """

    on_change: Optional[ControlEventHandler["CupertinoSegmentedButton"]] = None
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
