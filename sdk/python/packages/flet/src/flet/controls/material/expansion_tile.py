from enum import Enum
from typing import Annotated, Optional

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
from flet.utils.validation import V, ValidationRules

__all__ = ["ExpansionTile", "TileAffinity"]


class TileAffinity(Enum):
    """
    Where to place a control in controls that use :class:`~flet.ListTile` to position \
    a control next to a label.
    """

    LEADING = "leading"
    """
    Positions the control on the leading edge, and the secondary control, if any, on \
    the trailing edge.
    """

    TRAILING = "trailing"
    """
    Positions the control on the trailing edge, and the secondary control, if any, on \
    the leading edge.
    """

    PLATFORM = "platform"
    """
    Positions the control relative to the text in the fashion that is typical for the \
    current platform, and place the secondary control on the opposite side.
    """


@control("ExpansionTile")
class ExpansionTile(LayoutControl, AdaptiveControl):
    """
    A single-line ListTile with an expansion arrow icon that expands or collapses the \
    tile to reveal or hide its controls.

    Example:
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

    title: Annotated[
        StrOrControl,
        V.str_or_visible_control(),
    ]
    """
    A Control to display as primary content of this tile.

    Typically a :class:`~flet.Text` control.

    Raises:
        ValueError: If it is neither a string nor a visible `Control`.
    """

    controls: Optional[list[Control]] = None
    """
    The controls to be displayed when this tile :attr:`expanded`.

    Typically a list of :class:`~flet.ListTile` controls.
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the :attr:`title`.

    Typically a :class:`~flet.Text` control.
    """

    leading: Optional[IconDataOrControl] = None
    """
    A Control to display before the :attr:`title`.

    Typically a :class:`~flet.CircleAvatar` control.

    Depending on the value of :attr:`affinity`, this control
    may replace the rotating expansion arrow icon.
    """

    trailing: Optional[IconDataOrControl] = None
    """
    A Control to display after the :attr:`title`.

    Typically an :class:`~flet.Icon` control.

    Depending on the value of :attr:`affinity`, this control
    may replace the rotating expansion arrow icon.
    """

    controls_padding: Optional[PaddingValue] = None
    """
    Defines the padding around the :attr:`controls`.

    If `None`, :attr:`flet.ExpansionTileTheme.controls_padding` is used;
    if that is also `None`, then defaults to `Padding.all(0)`.
    """

    tile_padding: Optional[PaddingValue] = None
    """
    Defines the tile's padding.

    Analogous to :attr:`flet.ListTile.content_padding`, this property defines the
    insets for the :attr:`leading`, :attr:`title`, :attr:`subtitle` and
    :attr:`trailing` controls. It does not inset the expanded
    :attr:`controls` widgets.

    If `None`, :attr:`flet.ExpansionTileTheme.tile_padding` is used;
    if that is also `None`, then defaults to `Padding.symmetric(horizontal=16.0)`.
    """

    affinity: Optional[TileAffinity] = None
    """
    Typically used to force the expansion arrow icon to the tile's :attr:`leading` or \
    :attr:`trailing` edge.

    If `None`, :attr:`flet.ListTileTheme.affinity` is used;
    if that is also `None`, then defaults to :attr:`flet.TileAffinity.TRAILING`
    (the expansion arrow icon appears on the tile's trailing edge).
    """

    expanded_alignment: Optional[Alignment] = None
    """
    Defines the alignment of :attr:`controls`, which are arranged in a column when the \
    tile is expanded.

    If `None`, :attr:`flet.ExpansionTileTheme.expanded_alignment` is used;
    if that is also `None`, then defaults to :attr:`flet.Alignment.CENTER`.
    """

    expanded_cross_axis_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    """
    Defines the alignment of each child control within :attr:`controls` when the tile \
    is expanded.

    Raises:
        ValueError: If set to :attr:`flet.CrossAxisAlignment.BASELINE`.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Defines how the content of this tile is clipped.

    If set and a custom collapsed or expanded shape is provided,
    this value determines how this tile is clipped.

    If `None`, :attr:`flet.ExpansionTileTheme.clip_behavior` is used;
    if that is also `None`, then defaults to :attr:`flet.ClipBehavior.ANTI_ALIAS`.
    """

    maintain_state: bool = False
    """
    A boolean value which defines whether the state of the :attr:`controls` is \
    maintained when this tile :attr:`expanded` and collapses.

    When `True`, the children are kept in the tree while the tile is collapsed.
    When `False` (default), the :attr:`controls` are removed from the tree when
    the tile is collapsed and recreated upon expansion.
    """

    text_color: Optional[ColorValue] = None
    """
    The color of this tile's titles when the sublist is :attr:`expanded`.

    If `None`, :attr:`flet.ExpansionTileTheme.text_color` is used;
    if that is also `None`, then defaults to :attr:`~flet.TextTheme.body_large`
    of the :attr:`flet.Theme.text_theme`.
    """

    icon_color: Optional[ColorValue] = None
    """
    The icon color of this tile's expansion arrow icon when the sublist is \
    :attr:`expanded`.

    If `None`, :attr:`flet.ExpansionTileTheme.icon_color` is used;
    if that is also `None`, then defaults to :attr:`flet.ColorScheme.primary`
    of the :attr:`flet.Page.theme`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The border shape of this tile when the sublist is :attr:`expanded`.

    If `None`, :attr:`flet.ExpansionTileTheme.shape` is used;
    if that is also `None`, then defaults to a :class:`~flet.Border` with vertical sides
    of color :attr:`flet.Theme.divider_color`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color to display behind the sublist when :attr:`expanded`.

    If `None`, :attr:`flet.ExpansionTileTheme.bgcolor` is used;
    if that is also `None`, then defaults to :attr:`flet.Colors.TRANSPARENT`.
    """

    collapsed_bgcolor: Optional[ColorValue] = None
    """
    Defines the background color of this tile when the sublist is collapsed \
    (:attr:`expanded` is False).

    If `None`, :attr:`flet.ExpansionTileTheme.collapsed_bgcolor` is used;
    if that is also `None`, then defaults to :attr:`flet.Colors.TRANSPARENT`.
    """

    collapsed_icon_color: Optional[ColorValue] = None
    """
    The icon color of this tile's expansion arrow icon when the sublist is collapsed \
    (:attr:`expanded` is False).

    If `None`, :attr:`flet.ExpansionTileTheme.collapsed_icon_color` is used;
    if that is also `None`, then defaults to :attr:`flet.ColorScheme.on_surface`
    of the :attr:`flet.Page.theme`.
    """

    collapsed_text_color: Optional[ColorValue] = None
    """
    The color of this tile's titles when the sublist is collapsed (:attr:`expanded` is \
    False).

    If `None`, :attr:`flet.ExpansionTileTheme.collapsed_text_color` is used;
    if that is also `None`, then defaults to :attr:`~flet.TextTheme.body_large`
    of the :attr:`flet.Theme.text_theme`.
    """

    collapsed_shape: Optional[OutlinedBorder] = None
    """
    The tile's border shape when the sublist is collapsed.

    If `None`, :attr:`flet.ExpansionTileTheme.shape` is used;
    if that is also `None`, then defaults to a :class:`~flet.Border` with vertical sides
    of color :attr:`flet.Colors.TRANSPARENT`.
    """

    dense: Optional[bool] = None
    """
    Whether this list tile is part of a vertically dense list.

    Dense tiles default to having a smaller height.

    It is not recommended to set this property to `True` when in Material3.

    If `None`, then its value is based on :attr:`flet.ListTileTheme.dense`.
    """

    enable_feedback: bool = True
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. For \
    example, on Android a tap will produce a clicking sound and a long-press will \
    produce a short vibration, when feedback is enabled.
    """

    show_trailing_icon: bool = True
    """
    Whether this tile should build/show a default trailing icon, if :attr:`trailing` \
    is `None`.
    """

    min_tile_height: Optional[Number] = None
    """
    The minimum height of this tile.

    If `None`, the default tile heights are `56.0`, `72.0`, and `88.0` for one, two,
    and three lines of text respectively. If :attr:`dense` is `True`, these defaults
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
    Defines the animation style (curve and duration) for this tile's expansion and \
    collapse.

    If :attr:`flet.AnimationStyle.duration` is provided, it will be used to override
    the expansion animation duration. If it is `None`, then
    :attr:`flet.AnimationStyle.duration` from the
    :attr:`flet.ExpansionTileTheme.animation_style` will be used. If that is also
    `None`, `Duration(milliseconds=200)` will be used as default.

    If :attr:`flet.AnimationStyle.curve` is provided, it will be used to override
    the expansion animation curve. If it is `None`, then
    :attr:`flet.AnimationStyle.curve` from the
    :attr:`flet.ExpansionTileTheme.animation_style` will be used. If that is also
    `None`, :attr:`flet.AnimationCurve.EASE_IN` will be used as default.

    If :attr:`flet.AnimationStyle.reverse_curve` is provided, it will be used to \
    override
    the collapse animation curve. If it is `None`, then
    :attr:`flet.AnimationStyle.reverse_curve` from the
    :attr:`flet.ExpansionTileTheme.animation_style` will be used. If that is also
    `None`, the expansion curve will be used as default.

    Tip:
        To disable the animations, use
        :meth:`flet.AnimationStyle.no_animation`.
    """

    on_change: Optional[ControlEventHandler["ExpansionTile"]] = None
    """
    Called when a user clicks or taps the list tile.

    The :attr:`~flet.Event.data` property of the event handler argument is a boolean
    representing the :attr:`expanded` state of the tile after the change.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: (
                ctrl.expanded_cross_axis_alignment != CrossAxisAlignment.BASELINE
            ),
            message=(
                "expanded_cross_axis_alignment cannot be CrossAxisAlignment.BASELINE "
                "since the expanded controls are aligned in a column, not a row. "
                "Try aligning the controls differently."
            ),
        ),
    )
