from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
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
    """
    Where to place a control in controls that use [`ListTile`][flet.] to position a
    control next to a label.
    """

    LEADING = "leading"
    """
    Positions the control on the leading edge, and the secondary control, if
    any, on the trailing edge.
    """

    TRAILING = "trailing"
    """
    Positions the control on the trailing edge, and the secondary control, if
    any, on the leading edge.
    """

    PLATFORM = "platform"
    """
    Positions the control relative to the text in the fashion that is typical
    for the current platform, and place the secondary control on the opposite
    side.
    """


@control("ExpansionTile")
class ExpansionTile(LayoutControl, AdaptiveControl):
    """
    A single-line ListTile with an expansion arrow icon that expands or collapses the
    tile to reveal or hide its controls.

    ```python
    ft.ExpansionTile(
        width=400,
        title="Account",
        subtitle="Manage profile and security",
        expanded=True,
        controls=[
            ft.ListTile(title=ft.Text("Profile")),
            ft.ListTile(title=ft.Text("Security")),
        ],
    )
    ```
    """

    title: StrOrControl
    """
    A Control to display as primary content of this tile.

    Typically a [`Text`][flet.] control.

    Raises:
        ValueError: If it is neither a string nor a visible Control.
    """

    controls: Optional[list[Control]] = None
    """
    The controls to be displayed when this tile [expands][(c).expanded].

    Typically a list of [`ListTile`][flet.] controls.
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the [`title`][(c).].

    Typically a [`Text`][flet.] control.
    """

    leading: Optional[IconDataOrControl] = None
    """
    A Control to display before the [`title`][(c).].

    Typically a [`CircleAvatar`][flet.] control.

    Depending on the value of [`affinity`][(c).], this control
    may replace the rotating expansion arrow icon.
    """

    trailing: Optional[IconDataOrControl] = None
    """
    A Control to display after the [`title`][(c).].

    Typically an [`Icon`][flet.] control.

    Depending on the value of [`affinity`][(c).], this control
    may replace the rotating expansion arrow icon.
    """

    controls_padding: Optional[PaddingValue] = None
    """
    Defines the padding around the [`controls`][(c).].

    If `None`, [`ExpansionTileTheme.controls_padding`][flet.] is used;
    if that is also `None`, then defaults to `Padding.all(0)`.
    """

    tile_padding: Optional[PaddingValue] = None
    """
    Defines the tile's padding.

    Analogous to [`ListTile.content_padding`][flet.], this property defines the
    insets for the [`leading`][(c).], [`title`][(c).], [`subtitle`][(c).] and
    [`trailing`][(c).] controls. It does not inset the expanded
    [`controls`][(c).] widgets.

    If `None`, [`ExpansionTileTheme.tile_padding`][flet.] is used;
    if that is also `None`, then defaults to `Padding.symmetric(horizontal=16.0)`.
    """

    affinity: Optional[TileAffinity] = None
    """
    Typically used to force the expansion arrow icon to the tile's [`leading`][(c).] or
    [`trailing`][(c).] edge.

    If `None`, [`ListTileTheme.affinity`][flet.] is used;
    if that is also `None`, then defaults to [`TileAffinity.TRAILING`][flet.]
    (the expansion arrow icon appears on the tile's trailing edge).
    """

    expanded_alignment: Optional[Alignment] = None
    """
    Defines the alignment of [`controls`][(c).], which are arranged in a column when
    the tile is expanded.

    If `None`, [`ExpansionTileTheme.expanded_alignment`][flet.] is used;
    if that is also `None`, then defaults to [`Alignment.CENTER`][flet.].
    """

    expanded_cross_axis_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    """
    Defines the alignment of each child control within [`controls`][(c).] when the
    tile is expanded.

    Raises:
        ValueError: If set to [`CrossAxisAlignment.BASELINE`][flet.].
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Defines how the content of this tile is clipped.

    If set and a custom collapsed or expanded shape is provided,
    this value determines how this tile is clipped.

    If `None`, [`ExpansionTileTheme.clip_behavior`][flet.] is used;
    if that is also `None`, then defaults to [`ClipBehavior.ANTI_ALIAS`][flet.].
    """

    maintain_state: bool = False
    """
    A boolean value which defines whether the state of the [`controls`][(c).] is
    maintained when this tile [expands][(c).expanded] and collapses.

    When `True`, the children are kept in the tree while the tile is collapsed.
    When `False` (default), the [`controls`][(c).] are removed from the tree when
    the tile is collapsed and recreated upon expansion.
    """

    text_color: Optional[ColorValue] = None
    """
    The color of this tile's titles when the sublist is [`expanded`][(c).].

    If `None`, [`ExpansionTileTheme.text_color`][flet.] is used;
    if that is also `None`, then defaults to [`body_large`][flet.TextTheme.]
    of the [`Theme.text_theme`][flet.].
    """

    icon_color: Optional[ColorValue] = None
    """
    The icon color of this tile's expansion arrow icon
    when the sublist is [`expanded`][(c).].

    If `None`, [`ExpansionTileTheme.icon_color`][flet.] is used;
    if that is also `None`, then defaults to [`ColorScheme.primary`][flet.]
    of the [`Page.theme`][flet.].
    """

    shape: Optional[OutlinedBorder] = None
    """
    The border shape of this tile when the sublist is [`expanded`][(c).].

    If `None`, [`ExpansionTileTheme.shape`][flet.] is used;
    if that is also `None`, then defaults to a [`Border`][flet.] with vertical sides
    of color [`Theme.divider_color`][flet.].
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color to display behind the sublist when [`expanded`][(c).].

    If `None`, [`ExpansionTileTheme.bgcolor`][flet.] is used;
    if that is also `None`, then defaults to [`Colors.TRANSPARENT`][flet.].
    """

    collapsed_bgcolor: Optional[ColorValue] = None
    """
    Defines the background color of this tile when the sublist
    is collapsed ([`expanded`][(c).] is False).

    If `None`, [`ExpansionTileTheme.collapsed_bgcolor`][flet.] is used;
    if that is also `None`, then defaults to [`Colors.TRANSPARENT`][flet.].
    """

    collapsed_icon_color: Optional[ColorValue] = None
    """
    The icon color of this tile's expansion arrow icon when the sublist
    is collapsed ([`expanded`][(c).] is False).

    If `None`, [`ExpansionTileTheme.collapsed_icon_color`][flet.] is used;
    if that is also `None`, then defaults to [`ColorScheme.on_surface`][flet.]
    of the [`Page.theme`][flet.].
    """

    collapsed_text_color: Optional[ColorValue] = None
    """
    The color of this tile's titles when the sublist
    is collapsed ([`expanded`][(c).] is False).

    If `None`, [`ExpansionTileTheme.collapsed_text_color`][flet.] is used;
    if that is also `None`, then defaults to [`body_large`][flet.TextTheme.]
    of the [`Theme.text_theme`][flet.].
    """

    collapsed_shape: Optional[OutlinedBorder] = None
    """
    The tile's border shape when the sublist is collapsed.

    If `None`, [`ExpansionTileTheme.shape`][flet.] is used;
    if that is also `None`, then defaults to a [`Border`][flet.] with vertical sides
    of color [`Colors.TRANSPARENT`][flet.].
    """

    dense: Optional[bool] = None
    """
    Whether this list tile is part of a vertically dense list.

    Dense tiles default to having a smaller height.

    It is not recommended to set this property to `True` when in Material3.

    If `None`, then its value is based on [`ListTileTheme.dense`][flet.].
    """

    enable_feedback: bool = True
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. For
    example, on Android a tap will produce a clicking sound and a long-press will
    produce a short vibration, when feedback is enabled.
    """

    show_trailing_icon: bool = True
    """
    Whether this tile should build/show a default trailing icon, if
    [`trailing`][(c).] is `None`.
    """

    min_tile_height: Optional[Number] = None
    """
    The minimum height of this tile.

    If `None`, the default tile heights are `56.0`, `72.0`, and `88.0` for one, two,
    and three lines of text respectively. If [`dense`][(c).] is `True`, these defaults
    are changed to `48.0`, `64.0`, and `76.0`. A visual density value or a large title
    will also adjust the default tile heights.
    """

    expanded: bool = False
    """
    The expansion state of this tile.

    `True` - expanded, `False` - collapsed.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact this tile's layout will be.
    """

    animation_style: Optional[AnimationStyle] = None
    """
    Defines the animation style (curve and duration) for this tile's expansion and
    collapse.

    If [`AnimationStyle.duration`][flet.] is provided, it will be used to override
    the expansion animation duration. If it is `None`, then
    [`AnimationStyle.duration`][flet.] from the
    [`ExpansionTileTheme.animation_style`][flet.] will be used. If that is also
    `None`, `Duration(milliseconds=200)` will be used as default.

    If [`AnimationStyle.curve`][flet.] is provided, it will be used to override
    the expansion animation curve. If it is `None`, then
    [`AnimationStyle.curve`][flet.] from the
    [`ExpansionTileTheme.animation_style`][flet.] will be used. If that is also
    `None`, [`AnimationCurve.EASE_IN`][flet.] will be used as default.

    If [`AnimationStyle.reverse_curve`][flet.] is provided, it will be used to override
    the collapse animation curve. If it is `None`, then
    [`AnimationStyle.reverse_curve`][flet.] from the
    [`ExpansionTileTheme.animation_style`][flet.] will be used. If that is also
    `None`, the expansion curve will be used as default.

    Tip:
        To disable the animations, use
        [`AnimationStyle.no_animation()`][flet.AnimationStyle.no_animation].
    """

    on_change: Optional[ControlEventHandler["ExpansionTile"]] = None
    """
    Called when a user clicks or taps the list tile.

    The [`data`][flet.Event.] property of the event handler argument is a boolean
    representing the [`expanded`][(c).] state of the tile after the change.
    """

    def before_update(self):
        super().before_update()
        if isinstance(self.title, Control) and not self.title.visible:
            raise ValueError("title must be visible")
        if self.expanded_cross_axis_alignment == CrossAxisAlignment.BASELINE:
            raise ValueError(
                "expanded_cross_axis_alignment cannot be CrossAxisAlignment.BASELINE "
                "since the expanded controls are aligned in a column, not a row. "
                "Try aligning the controls differently."
            )
