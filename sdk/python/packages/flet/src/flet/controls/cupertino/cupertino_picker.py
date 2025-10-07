from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["CupertinoPicker"]


@control("CupertinoPicker")
class CupertinoPicker(LayoutControl):
    """
    An iOS-styled picker.
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of controls representing items in this picker.
    """

    item_extent: Number = 32.0
    """
    The uniform height of all [`controls`][(c).].

    Raises:
        ValueError: If [`item_extent`][(c).] is not strictly greater than `0.0`.
    """

    selected_index: int = 0
    """
    The index (starting from `0`) of the selected item in the [`controls`][(c).] list.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this timer picker.
    """

    use_magnifier: bool = False
    """
    Whether to use the magnifier for the center item of this picker's wheel.
    """

    looping: bool = False
    """
    If `True`, children on a wheel can be scrolled in a loop.
    """

    magnification: Number = 1.0
    """
    The zoomed-in or magnification rate of the magnifier.

    If the value is greater than `1.0`, the item in the center will be zoomed in by that
    rate, and it will also be rendered as flat, not cylindrical like the rest of the
    list. The item will be zoomed-out if magnification is less than `1.0`.

    Note:
        Has effect only if [`use_magnifier`][(c).] is `True`.

    Raises:
        ValueError: If [`magnification`][(c).] is not strictly greater than `0.0`.
    """

    squeeze: Number = 1.45
    """
    The angular compactness of the children on the wheel.

    Raises:
        ValueError: If [`squeeze`][(c).] is not strictly greater than `0.0`.
    """

    diameter_ratio: Number = 1.07
    """
    Relative ratio between this picker's height and the simulated cylinder's diameter.

    Smaller values create more pronounced curvatures in the scrollable wheel.
    """

    off_axis_fraction: Number = 0.0
    """
    How much the wheel is horizontally off-center, as a fraction of its width.
    """

    selection_overlay: Optional[Control] = None
    """
    A control overlaid on the picker to highlight the selected entry, centered and
    matching the height of the center row.

    Defaults to a rounded rectangle in iOS 14 style with
    [`default_selection_overlay_bgcolor`][(c).] as background color.
    """

    default_selection_overlay_bgcolor: ColorValue = CupertinoColors.TERTIARY_SYSTEM_FILL
    """
    The default background color of the [`selection_overlay`][(c).].
    """

    on_change: Optional[ControlEventHandler["CupertinoPicker"]] = None
    """
    Called when the selection changes.
    """

    def before_update(self):
        super().before_update()
        if self.squeeze <= 0.0:
            raise ValueError(
                f"squeeze must be strictly greater than 0.0, got {self.squeeze}"
            )
        if self.magnification <= 0.0:
            raise ValueError(
                f"magnification must be strictly greater than 0.0, "
                f"got {self.magnification}"
            )
        if self.item_extent <= 0.0:
            raise ValueError(
                f"item_extent must be strictly greater than 0.0, got {self.item_extent}"
            )
