from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.types import (
    ColorValue,
    Number,
    OptionalColorValue,
)

__all__ = ["CupertinoPicker"]


@control("CupertinoPicker")
class CupertinoPicker(ConstrainedControl):
    """
    An iOS-styled picker.

    Online docs: https://flet.dev/docs/controls/cupertinopicker
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of controls representing items in this picker.
    """

    item_extent: Number = 32.0
    """
    The uniform height of all children.

    Defaults to `32`.
    """

    selected_index: int = 0
    """
    The index (starting from 0) of the selected item in the `controls` list.
    """

    bgcolor: OptionalColorValue = None
    """
    The background [color](https://flet.dev/docs/reference/colors) of the timer picker.
    """

    use_magnifier: bool = False
    """
    Whether to use the magnifier for the center item of the wheel.
    """

    looping: bool = False
    """
    If `True`, children on a wheel can be scrolled in a loop.

    Defaults to `False`.
    """

    magnification: Number = 1.0
    """
    The zoomed-in rate of the magnifier, if it is used.

    If the value is greater than `1.0`, the item in the center will be zoomed in by that
    rate, and it will also be rendered as flat, not cylindrical like the rest of the 
    list. The item will be zoomed-out if magnification is less than `1.0`.

    Defaults to `1.0` - normal.
    """

    squeeze: Number = 1.45
    """
    The angular compactness of the children on the wheel.
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
    `default_selection_overlay_bgcolor` as background color.
    """

    default_selection_overlay_bgcolor: ColorValue = CupertinoColors.TERTIARY_SYSTEM_FILL
    """
    The default background [color](https://flet.dev/docs/reference/colors) of the 
    `selection_overlay`.

    Defaults to `CupertinoColors.TERTIARY_SYSTEM_FILL`.
    """

    on_change: OptionalControlEventHandler["CupertinoPicker"] = None
    """
    Fires when the selection changes.
    """

    def before_update(self):
        super().before_update()
        assert self.squeeze > 0, "squeeze must be strictly greater than 0"
        assert self.magnification > 0, "magnification must be strictly greater than 0"
        assert self.item_extent is None or self.item_extent > 0, (
            "item_extent must be strictly greater than 0"
        )
