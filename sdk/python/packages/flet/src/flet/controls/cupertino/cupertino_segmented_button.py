from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import ColorValue

__all__ = ["CupertinoSegmentedButton"]


@control("CupertinoSegmentedButton")
class CupertinoSegmentedButton(LayoutControl):
    """
    An iOS-style segmented button.

    ```python
    ft.CupertinoSegmentedButton(
        controls=[
            ft.Text("One"),
            ft.Text("Two"),
            ft.Text("Three"),
        ],
        selected_index=1,
    )
    ```
    """

    controls: list[Control]
    """
    The list of segments to be displayed.

    Note:
        Must contain at least two visible Controls.

    Raises:
        ValueError: If [`controls`][(c).] does not contain at least two visible
            controls.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected segment in the
    [`controls`][(c).] list.

    Raises:
        IndexError: If [`selected_index`][(c).] is out of range relative to the
            visible controls.
    """

    selected_color: Optional[ColorValue] = None
    """
    The color of this button when it is selected.
    """

    unselected_color: Optional[ColorValue] = None
    """
    The color of this button when it is not selected.
    """

    border_color: Optional[ColorValue] = None
    """
    The color of this button's border.
    """

    padding: Optional[PaddingValue] = None
    """
    This button's padding.
    """

    click_color: Optional[ColorValue] = None
    """
    The color used to fill the background
    of this control when temporarily interacting with through a long press or drag.

    Defaults to the [`selected_color`][(c).]
    with 20% opacity.
    """

    disabled_color: Optional[ColorValue] = None
    """
    The color used to fill the background of the segment when it is disabled.

    If `None`, this color will be 50% opacity of the
    [`selected_color`][(c).] when
    the segment is selected. If the segment is unselected, this color will be
    set to the [`unselected_color`][(c).].
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
