from typing import Optional

from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.types import ClipBehavior, OptionalColorValue, OptionalNumber


@control("BottomSheet")
class BottomSheet(DialogControl):
    """
    A modal bottom sheet is an alternative to a menu or a dialog and prevents the user
    from interacting with the rest of the app.

    Online docs: https://flet.dev/docs/controls/bottomsheet
    """

    content: Control
    """
    The content `Control` of the bottom sheet.
    """

    elevation: OptionalNumber = None
    """
    Controls the size of the shadow below the BottomSheet.
    """

    bgcolor: OptionalColorValue = None
    """
    The sheet's background [color](https://flet.dev/docs/reference/colors).
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

    Defaults to `False`.
    """

    is_scroll_controlled: bool = False
    """
    Specifies if the bottom sheet contains scrollable content, such as ListView or 
    GridView.

    Defaults to `False`.
    """

    maintain_bottom_view_insets_padding: bool = True
    """
    Adds a padding at the bottom to avoid obstructing bottom sheet content with 
    on-screen keyboard or other system elements.
    """

    animation_style: Optional[AnimationStyle] = None
    """
    The sheet's animation style.

    Value is of type [`AnimationStyle`](https://flet.dev/docs/reference/types/animationstyle).
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    The size constraints to apply to the bottom sheet.

    Value is of type [`BoxConstraints`](https://flet.dev/docs/reference/types/boxconstraints).
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The sheet's clip behavior.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior).
    """

    shape: Optional[OutlinedBorder] = None
    """
    Defines the shape of the bottom sheet.

    Value is of type [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder).
    """

    def before_update(
        self,
    ):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
