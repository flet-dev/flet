from enum import Enum
from typing import List, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    ClipBehavior,
    CrossAxisAlignment,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    VisualDensity,
)

__all__ = ["ExpansionTile", "TileAffinity"]


class TileAffinity(Enum):
    LEADING = "leading"
    TRAILING = "trailing"
    PLATFORM = "platform"


@control("ExpansionTile")
class ExpansionTile(ConstrainedControl, AdaptiveControl):
    """
    A single-line ListTile with an expansion arrow icon that expands or collapses the tile to reveal or hide its controls.

    -----

    Online docs: https://flet.dev/docs/controls/expansiontile
    """

    title: Control
    controls: Optional[List[Control]] = None
    subtitle: Optional[Control] = None
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    controls_padding: OptionalPaddingValue = None
    tile_padding: OptionalPaddingValue = None
    affinity: Optional[TileAffinity] = None
    expanded_alignment: Optional[Alignment] = None
    expanded_cross_axis_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    clip_behavior: Optional[ClipBehavior] = None
    initially_expanded: bool = False
    maintain_state: bool = False
    text_color: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    shape: Optional[OutlinedBorder] = None
    bgcolor: OptionalColorValue = None
    collapsed_bgcolor: OptionalColorValue = None
    collapsed_icon_color: OptionalColorValue = None
    collapsed_text_color: OptionalColorValue = None
    collapsed_shape: Optional[OutlinedBorder] = None
    dense: bool = None
    enable_feedback: bool = True
    show_trailing_icon: bool = True
    min_tile_height: OptionalNumber = None
    visual_density: Optional[VisualDensity] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.title.visible, "title must be visible"
