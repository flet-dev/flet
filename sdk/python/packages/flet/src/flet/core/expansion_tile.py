from dataclasses import field
from enum import Enum
from typing import List, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    CrossAxisAlignment,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
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
    controls_padding: Optional[PaddingValue] = None
    tile_padding: Optional[PaddingValue] = None
    affinity: Optional[TileAffinity] = None
    expanded_alignment: Optional[Alignment] = None
    expanded_cross_axis_alignment: CrossAxisAlignment = field(
        default_factory=lambda: CrossAxisAlignment.CENTER
    )
    clip_behavior: Optional[ClipBehavior] = None
    initially_expanded: Optional[bool] = field(default=False)
    maintain_state: Optional[bool] = field(default=False)
    text_color: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    shape: Optional[OutlinedBorder] = None
    bgcolor: Optional[ColorValue] = None
    collapsed_bgcolor: Optional[ColorValue] = None
    collapsed_icon_color: Optional[ColorValue] = None
    collapsed_text_color: Optional[ColorValue] = None
    collapsed_shape: Optional[OutlinedBorder] = None
    dense: Optional[bool] = None
    enable_feedback: Optional[bool] = field(default=True)
    show_trailing_icon: Optional[bool] = field(default=True)
    min_tile_height: OptionalNumber = None
    visual_density: Optional[VisualDensity] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.title.visible, "title must be visible"
