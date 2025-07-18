from typing import Optional

from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.types import ClipBehavior, ColorValue, Number

__all__ = ["BottomSheet"]


@control("BottomSheet")
class BottomSheet(DialogControl):
    """
    Displays a modal bottom sheet.

    A bottom sheet is an alternative to a menu or dialog and prevents the user
    from interacting with the rest of the app.

    Raises:
        AssertionError: If [`elevation`][(c).] is negative.
    """

    content: Control
    """
    The content of this bottom sheet.
    """

    elevation: Optional[Number] = None
    """
    Defines the size of the shadow below the bottom sheet.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The sheet's background color.
    """

    dismissible: bool = True
    """
    Specifies whether the bottom sheet will be dismissed when user taps on the scrim.
    """

    enable_drag: bool = False
    """
    Specifies whether the bottom sheet can be dragged up and down and dismissed by
    swiping downwards.
    """

    show_drag_handle: bool = False
    """
    Whether to display drag handle at the top of sheet or not.
    """

    use_safe_area: bool = True
    """
    Specifies whether the sheet will avoid system intrusions on the top, left, and
    right.
    """

    scroll_controlled: bool = False
    """
    Specifies if the bottom sheet contains scrollable content, such as ListView or
    GridView.
    """

    maintain_bottom_view_insets_padding: bool = True
    """
    Adds a padding at the bottom to avoid obstructing bottom sheet content with
    on-screen keyboard or other system elements.
    """

    animation_style: Optional[AnimationStyle] = None
    """
    The sheet's animation style.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    The size constraints to apply to the bottom sheet.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Defines how the content of the bottom sheet should be clipped.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Defines the shape of the bottom sheet.
    """

    barrier_color: Optional[ColorValue] = None
    """
    The color of the scrim that obscures content behind this bottom sheet.
    """

    def before_update(self):
        super().before_update()
        assert self.elevation is None or self.elevation >= 0, (
            f"elevation must be greater than or equal to zero, got {self.elevation}"
        )
