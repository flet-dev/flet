from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    CrossAxisAlignment,
    IconDataOrControl,
    Number,
    StrOrControl,
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
    A single-line ListTile with an expansion arrow icon that expands or collapses the
    tile to reveal or hide its controls.
    """

    title: StrOrControl
    """
    A `Control` to display as primary content of the tile.

    Typically a [`Text`][flet.Text] control.
    """

    controls: Optional[list[Control]] = None
    """
    The controls to be displayed when the tile expands.

    Typically a list of [`ListTile`][flet.ListTile] controls.
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the title.

    Typically a [`Text`][flet.Text] control.
    """

    leading: Optional[IconDataOrControl] = None
    """
    A `Control` to display before the title.
    """

    trailing: Optional[IconDataOrControl] = None
    """
    A `Control` to display after the title.

    Typically an [`Icon`][flet.Icon] control.
    """

    controls_padding: Optional[PaddingValue] = None
    """
    Defines the padding around the `controls`.
    """

    tile_padding: Optional[PaddingValue] = None
    """
    Defines the tile's padding. Default value is `Padding.symmetric(horizontal=16.0)`.
    """

    affinity: Optional[TileAffinity] = None
    """
    Typically used to force the expansion arrow icon to the tile's `leading` or
    `trailing` edge.

    Defaults to `TileAffinity.PLATFORM`.
    """

    expanded_alignment: Optional[Alignment] = None
    """
    Defines the alignment of children, which are arranged in a column when the tile is
    expanded.
    """

    expanded_cross_axis_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    """
    Defines the alignment of each child control within `controls` when the tile is
    expanded.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option.

    Defaults to `ClipBehavior.NONE`.
    """

    initially_expanded: bool = False
    """
    A boolean value which defines whether the tile is initially expanded or collapsed.

    Defaults to `False`.
    """

    maintain_state: bool = False
    """
    A boolean value which defines whether the state of the `controls` is maintained
    when the tile expands and collapses.

    Defaults to `False`.
    """

    text_color: Optional[ColorValue] = None
    """
    The color of the tile's titles when the
    sublist is expanded.
    """

    icon_color: Optional[ColorValue] = None
    """
    The icon color of tile's expansion arrow
    icon when the sublist is expanded.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The tile's border shape when the sublist is expanded.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The  color to display behind the sublist
    when expanded.
    """

    collapsed_bgcolor: Optional[ColorValue] = None
    """
    Defines the background color of tile when
    the sublist is collapsed.
    """

    collapsed_icon_color: Optional[ColorValue] = None
    """
    The icon color of tile's expansion arrow
    icon when the sublist is collapsed.
    """

    collapsed_text_color: Optional[ColorValue] = None
    """
    The color of the tile's titles when the
    sublist is collapsed.
    """

    collapsed_shape: Optional[OutlinedBorder] = None
    """
    The tile's border shape when the sublist is collapsed. The value is an instance
    of [`OutlinedBorder`][flet.OutlinedBorder]
    """

    dense: Optional[bool] = None
    """
    Whether this list tile is part of a vertically dense list. Dense list tiles default
    to a smaller height.

    It is not recommended to set this property to `True` when in Material3.
    """

    enable_feedback: bool = True
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. For
    example, on Android a tap will produce a clicking sound and a long-press will
    produce a short vibration, when feedback is enabled.

    Defaults to `True`.
    """

    show_trailing_icon: bool = True
    """
    Whether to show the trailing icon (be it the default icon or the custom `trailing`,
    if specified and visible).

    Defaults to `True`.
    """

    min_tile_height: Optional[Number] = None
    """
    The minimum height of the tile.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the control's layout will be.
    """

    on_change: Optional[ControlEventHandler["ExpansionTile"]] = None
    """
    Called when a user clicks or taps the list tile.
    """

    def before_update(self):
        super().before_update()
        if isinstance(self.title, Control):
            assert self.title.visible, "title must be visible"
