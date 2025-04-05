from dataclasses import field
from typing import List, Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["CupertinoPicker"]


@control("CupertinoPicker")
class CupertinoPicker(ConstrainedControl):
    """
    An iOS-styled picker.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinopicker
    """

    controls: List[Control] = field(default_factory=list)
    item_extent: OptionalNumber = None
    selected_index: int = 0
    bgcolor: OptionalColorValue = None
    use_magnifier: bool = False
    looping: bool = False
    magnification: Number = 1.0
    squeeze: Number = 1.45
    diameter_ratio: Number = 1.07
    off_axis_fraction: Number = 0.0
    selection_overlay: Optional[Control] = None
    default_selection_overlay_bgcolor: OptionalColorValue = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.squeeze > 0, "squeeze must be strictly greater than 0"
        assert self.magnification > 0, "magnification must be strictly greater than 0"
        assert (
            self.item_extent is None or self.item_extent > 0
        ), "item_extent must be strictly greater than 0"
