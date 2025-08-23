from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.colors import Colors
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler, Event, EventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import Duration, DurationValue
from flet.controls.margin import MarginValue
from flet.controls.material.form_field_control import IconDataOrControl
from flet.controls.padding import Padding, PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MouseCursor,
    Number,
    StrOrControl,
)

__all__ = [
    "Tab",
    "TabAlignment",
    "TabBar",
    "TabBarHoverEvent",
    "TabBarIndicatorSize",
    "TabBarView",
    "TabIndicatorAnimation",
    "Tabs",
    "UnderlineTabIndicator",
]


class TabAlignment(Enum):
    """
    Defines how tabs are aligned horizontally in a [`Tabs`][flet.Tabs].
    """

    START = "start"
    """
    If [`TabBar.scrollable`][flet.TabBar.scrollable] is `True`,
    tabs are aligned to the start of the [`TabBar`][flet.TabBar].
    """

    START_OFFSET = "startOffset"
    """
    If [`TabBar.scrollable`][flet.TabBar.scrollable] is `True`,
    tabs are aligned to the start of the
    [`TabBar`][flet.TabBar] with an offset of `52.0` pixels.
    """

    FILL = "fill"
    """
    If [`TabBar.scrollable`][flet.TabBar.scrollable] is `False`,
    tabs are stretched to fill the [`TabBar`][flet.TabBar].
    """

    CENTER = "center"
    """
    Tabs are aligned to the center of the [`TabBar`][flet.TabBar].
    """


class TabIndicatorAnimation(Enum):
    """
    Defines how the tab indicator animates when the selected tab changes.
    """

    LINEAR = "linear"
    """
    The tab indicator animates linearly.
    """

    ELASTIC = "elastic"
    """
    The tab indicator animates with an elastic effect.
    """


class TabBarIndicatorSize(Enum):
    """
    Defines how the bounds of the selected tab indicator are computed.
    """

    TAB = "tab"
    """
    The tab indicator's bounds are as wide as the space occupied by the tab
    in the tab bar: from the right edge of the previous tab to the left edge
    of the next tab.
    """

    LABEL = "label"
    """
    The tab's bounds are only as wide as the (centered) tab widget itself.

    This value is used to align the tab's label, typically a [Tab]
    widget's text or icon, with the selected tab indicator.
    """


@dataclass
class TabBarHoverEvent(Event["TabBar"]):
    hovering: bool
    """
    Whether a pointer has entered (`True`) or exited (`False`) the tab bar
    at [`index`][flet.TabBarHoverEvent.index].
    """

    index: int
    """
    The index of the tab that is being hovered over.
    """


@dataclass
class UnderlineTabIndicator:
    border_side: BorderSide = field(
        default_factory=lambda: BorderSide(width=2.0, color=Colors.WHITE)
    )
    """
    The color and weight of the horizontal line drawn below the selected tab.
    """

    insets: PaddingValue = field(default_factory=lambda: Padding.zero())
    """
    Locates the selected tab's underline relative to the tab's boundary.

    The [`TabBar.indicator_size`][flet.TabBar.indicator_size] property can be used
    to define the tab indicator's bounds in terms of its (centered) tab control with
    [`TabBarIndicatorSize.LABEL`][flet.TabBarIndicatorSize.LABEL], or the entire tab
    with [`TabBarIndicatorSize.TAB`][flet.TabBarIndicatorSize.TAB].
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The radius of the indicator's corners.

    If this value is not `None`, a rounded rectangular tab indicator is
    drawn, otherwise rectangular tab indicator is drawn.
    """


@control("Tabs")
class Tabs(ConstrainedControl, AdaptiveControl):
    """
    Used for navigating frequently accessed, distinct content
    categories. Tabs allow for navigation between two or more content views and relies
    on text headers to articulate the different sections of content.

    Raises:
        ValueError: If [`length`][flet.Tabs.length] is negative.
        IndexError: If [`selected_index`][(c).] is not in the range
            `[-length, length - 1]`.
    """

    content: Control
    """
    The content to display.
    """

    length: int
    """
    The total number of tabs.

    Typically greater than one.

    Note:
        Must match the length of both [`TabBar.tabs`][flet.TabBar.tabs]
        and [`TabBarView.controls`][flet.TabBarView.controls]. Don't forget to update
        it when adding/removing tabs.
    """

    selected_index: int = 0
    """
    The index of the currently selected tab.

    Supports Python-style negative indexing, where `-1` represents the last tab,
    `-2` the second to last, and so on.

    Note:
        - Must be in range `[-length, length - 1]`.
        - Changing the value of this property will internally trigger
            [`move_to`][flet.Tabs.move_to] with
            [`animation_duration`][flet.Tabs.animation_duration] and
            [`Curve.EASE`][flet.AnimationCurve.EASE] animation curve. To specify
            a different animation curve or duration for this particular change,
            use [`move_to`][flet.Tabs.move_to] directly.
    """

    animation_duration: DurationValue = field(
        default_factory=lambda: Duration(milliseconds=100),
    )
    """
    The duration of tab animations. For example, the animation that occurs
    when the selected tab changes.
    """

    on_change: Optional[ControlEventHandler["Tabs"]] = None
    """
    Called when [`selected_index`][flet.Tabs.selected_index] changes.

    The [`data`][flet.Event.data] property of the event handler argument
    contains the index of the selected tab.
    """

    def before_update(self):
        super().before_update()
        if self.length < 0:
            raise ValueError(
                f"length must be greater than or equal to 0, got {self.length}"
            )
        if not (-self.length <= self.selected_index < self.length):
            raise IndexError(
                f"selected_index out of range: got {self.selected_index}, "
                f"expected in range [-{self.length}, {self.length - 1}]"
            )

    async def move_to(
        self,
        index: int,
        animation_curve: AnimationCurve = AnimationCurve.EASE_IN,
        animation_duration: Optional[DurationValue] = None,
    ):
        """
        Selects the tab at the given `index`.

        Additionally, it triggers [`on_change`][flet.Tabs.on_change] event and updates
        [`selected_index`][flet.Tabs.selected_index].

        Note:
            If `index` is negative, it is interpreted as a Python-style negative index
            (e.g., -1 refers to the last tab). If the resolved index is already the
            currently selected tab, the method returns immediately and does nothing.

        Args:
            index: The index of the tab to select. Must be between in range
                `[-length, length - 1]`.
            animation_curve: The curve to apply to the animation.
            animation_duration: The duration of the animation. If `None` (the default),
                [`Tabs.animation_duration`][flet.Tabs.animation_duration] will be used.

        Raises:
            IndexError: If the `index` is outside the range `[-length, length - 1]`.
        """
        if not (-self.length <= index < self.length):
            raise IndexError(
                f"index out of range: got {index}, expected in range "
                f"[-{self.length}, {self.length - 1}]"
            )

        # Resolve negative index to positive
        resolved_index = index if index >= 0 else self.length + index

        # Early return if already on this tab
        if self.selected_index == resolved_index:
            return

        await self._invoke_method(
            method_name="move_to",
            arguments={
                "index": index,
                "curve": animation_curve,
                "duration": animation_duration
                if animation_duration is not None
                else self.animation_duration,
            },
        )


@control("TabBarView")
class TabBarView(ConstrainedControl, AdaptiveControl):
    """
    A page view with one child per tab.

    Note:
        The length of [`controls`][(c).] must be the same as the
        [`length`][flet.Tabs.length] property of the ancestor [`Tabs`][flet.Tabs].
    """

    controls: list[Control]
    """
    A list of controls, where each control represents the
    content of a corresponding tab. So, a control at index `i` in this list is
    displayed when the [`Tab`][flet.Tab] at index `i` is selected.

    Note:
        The length of this list must be equal to the number of tabs specified in an
        ancestor [`Tabs`][flet.Tabs] control.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    Defines how the [`controls`][flet.TabBarView.controls] will be clipped.
    """

    viewport_fraction: Number = 1.0
    """
    The fraction of the viewport that each page should occupy.

    For example, `1.0` (the default), means each page fills
    the viewport in the scrolling direction.
    """


@control("TabBar")
class TabBar(ConstrainedControl, AdaptiveControl):
    """
    Used for navigating frequently accessed, distinct content
    categories. Tabs allow for navigation between two or more content views and relies
    on text headers to articulate the different sections of content.

    Raises:
        AssertionError: If [`indicator`][(c).] is None and
            [`indicator_thickness`][(c).] is not strictly greater than 0.
        AssertionError: If [`tab_alignment`][(c).] is not valid for
            the given [`scrollable`][(c).] state.
    """

    tabs: list[Control]
    """
    A list of controls.

    Typically [`Tab`][flet.Tab]s.
    """

    scrollable: bool = True
    """
    Whether this tab bar can be scrolled horizontally.

    If `True`, then each tab is as wide as needed for its label and
    the entire tab bar is scrollable. Otherwise each tab gets an equal share
    of the available space.
    """

    tab_alignment: Optional[TabAlignment] = None
    """
    Specifies the horizontal alignment of the tabs within this tab bar.

    If this is `None`, then the value of
    [`TabBarTheme.tab_alignment`][flet.TabBarTheme.tab_alignment] is used.
    If [`TabBarTheme.tab_alignment`][flet.TabBarTheme.tab_alignment] is `None` and
    [`Theme.use_material3`][flet.Theme.use_material3] is `True`,
    then [TabAlignment.START_OFFSET][flet.TabAlignment.START_OFFSET] is used if
    [`scrollable`][flet.TabBar.scrollable] is `True`,
    otherwise [`TabAlignment.FILL`][flet.TabAlignment.FILL] is used.

    If [`TabBarTheme.tab_alignment`][flet.TabBarTheme.tab_alignment] is `None`
    and [`Theme.use_material3`][flet.Theme.use_material3] is `False`,
    then [`TabAlignment.CENTER`][flet.TabAlignment.CENTER] is used if
    [`scrollable`][flet.TabBar.scrollable] is `True`,
    otherwise [`TabAlignment.FILL`][flet.TabAlignment.FILL] is used.

    Note:
        - If [`scrollable`][flet.TabBar.scrollable] is `False`, then
            [`tab_alignment`][flet.TabBar.tab_alignment] must be either
            [`TabAlignment.FILL`][flet.TabAlignment.FILL] or
            [`TabAlignment.CENTER`][flet.TabAlignment.CENTER].
        - If [`scrollable`][flet.TabBar.scrollable] is `True`, then
            [`tab_alignment`][flet.TabBar.tab_alignment] must be
            [`TabAlignment.START`][flet.TabAlignment.START],
            [`TabAlignment.START_OFFSET`][flet.TabAlignment.START_OFFSET]
            or [`TabAlignment.CENTER`][flet.TabAlignment.CENTER].
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the indicator(line that appears below the selected tab).

    Note:
        Will be ignored if [`indicator`][flet.TabBar.indicator] or
        [`TabBarTheme.indicator`][flet.TabBarTheme.indicator] is not `None`.
    """

    indicator: Optional[UnderlineTabIndicator] = None
    """
    Defines the appearance of the selected tab indicator.

    If this or [`TabBarTheme.indicator`][flet.TabBarTheme.indicator] is not `None`,
    [`indicator_color`][flet.TabBar.indicator_color] and
    [`indicator_thickness`][flet.TabBar.indicator_thickness] properties are ignored.

    The indicator's size is based on the tab's bounds. If
    [`indicator_size`][flet.TabBar.indicator_size]
    is [`TabBarIndicatorSize.TAB`][flet.TabBarIndicatorSize.TAB],
    the tab's bounds are as wide as the space occupied by the tab in the tab bar.
    If [`indicator_size`][flet.TabBar.indicator_size] is
    [`TabBarIndicatorSize.LABEL`][flet.TabBarIndicatorSize.LABEL],
    then the tab's bounds are only as wide as the tab control itself.
    """

    indicator_size: Optional[TabBarIndicatorSize] = None
    """
    Defines how the selected tab indicator's size is computed.

    The size of the selected tab indicator is defined relative to the
    tab's overall bounds if `indicator_size` is
    [`TabBarIndicatorSize.TAB`][flet.TabBarIndicatorSize.TAB]
    (the default) or relative to the bounds of the tab's control if
    `indicator_size` is [`TabBarIndicatorSize.LABEL`][flet.TabBarIndicatorSize.LABEL].

    The selected tab's location appearance can be refined further with
    the [`indicator_color`][flet.TabBar.indicator_color],
    [`indicator_thickness`][flet.TabBar.indicator_thickness],
    and [`indicator`][flet.TabBar.indicator] properties.
    """

    indicator_animation: Optional[TabIndicatorAnimation] = None
    """
    Specifies the animation behavior of the tab indicator.

    If this is `None`, then the value of
    [`TabBarTheme.indicator_animation`][flet.TabBarTheme.indicator_animation] is used.
    If that is also `None`, then the tab indicator will animate linearly if the
    [`indicator_size`][flet.TabBar.indicator_size] is
    [`TabBarIndicatorSize.TAB`][flet.TabBarIndicatorSize.TAB], otherwise it will animate
    with an elastic effect if the [`indicator_size`][flet.TabBar.indicator_size] is
    [`TabBarIndicatorSize.LABEL`][flet.TabBarIndicatorSize.LABEL].
    """

    secondary: bool = False
    """
    Whether to create a secondary/nested tab bar.

    Secondary tabs are used within a content area to further separate related content
    and establish hierarchy.
    """

    label_color: Optional[ColorValue] = None
    """
    The color of selected tab labels.
    """

    label_padding: Optional[PaddingValue] = None
    """
    The padding around the tab label.
    """

    label_text_style: Optional[TextStyle] = None
    """
    The text style of the tab labels.
    """

    unselected_label_color: Optional[ColorValue] = None
    """
    The color of unselected tab labels.
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    The text style of the unselected tab labels.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Defines the ink response focus, hover, and splash
    colors in various [`ControlState`][flet.ControlState] states.

    The following states are supported: `ControlState.PRESSED`,
    `ControlState.HOVERED` and
    `ControlState.FOCUSED`.
    """

    divider_height: Optional[Number] = None
    """
    The height of the divider.

    If `None`, defaults to
    [`TabBarTheme.divider_height`][flet.TabBarTheme.divider_height]. If this is also
    `None`, `1.0` will be used.
    """

    indicator_thickness: Number = 2.0
    """
    The thickness of the indicator. Value must be greater than zero.

    Note:
        Will be ignored if [`indicator`][flet.TabBar.indicator] or
        [`TabBarTheme.indicator`][flet.TabBarTheme.indicator] is not `None`.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback.

    On Android, for example, setting this to `True` produce a click sound and a
    long-press will produce a short vibration.

    Defaults to `True`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this
    control.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding around the Tabs control.
    """

    splash_border_radius: Optional[BorderRadiusValue] = None
    """
    Defines the clipping radius of splashes that extend outside the bounds of the tab.
    """

    on_click: Optional[ControlEventHandler["TabBar"]] = None
    """
    Called when a tab is clicked.

    The [`data`][flet.Event.data] property of the event handler argument
    contains the index of the clicked tab.
    """

    on_hover: Optional[EventHandler[TabBarHoverEvent]] = None
    """
    Called when a tab's (from [`tabs`][flet.TabBar.tabs]) hover state in the
    tab bar changes.

    When hover is moved from one tab directly to another, this will be called
    twice. First to represent hover exiting the initial tab, and then second
    for the pointer entering hover over the next tab.
    """

    def __contains__(self, item):
        return item in self.tabs

    def before_update(self):
        super().before_update()
        assert self.indicator is not None or self.indicator_thickness > 0.0, (
            f"indicator_thickness must be strictly greater than zero if indicator is "
            f"None, got {self.indicator_thickness}"
        )
        valid_alignments = (
            [TabAlignment.CENTER, TabAlignment.FILL]
            if not self.scrollable
            else [TabAlignment.START, TabAlignment.START_OFFSET, TabAlignment.CENTER]
        )

        assert self.tab_alignment is None or self.tab_alignment in valid_alignments, (
            f"If scrollable is {self.scrollable}, tab_alignment must be one of: "
            f"{', '.join(f'TabAlignment.{a.name}' for a in valid_alignments)}."
        )


@control("Tab")
class Tab(AdaptiveControl):
    """
    A Material Design [`TabBar`][flet.TabBar] tab.

    Raises:
        AssertionError: If both [`label`][(c).] and [`icon`][(c).] are not set.
    """

    label: Optional[StrOrControl] = None
    """
    The tab's name. Can be either a string or a control.
    """

    icon: Optional[IconDataOrControl] = None
    """
    An icon to display on the left of Tab text.
    """

    height: Optional[Number] = None
    """
    The height of the tab.

    If `None`, it will be calculated based on the content of the Tab. When
    [`icon`][flet.Tab.icon] is not `None` along with [`label`][flet.Tab.label],
    the default `height` is `72.0` pixels. Without an `icon`,
    the `height` is 46.0 pixels.

    Currently, the provided tab height cannot be lower than the default height.
    """

    icon_margin: Optional[MarginValue] = None
    """
    The margin added around the tab's icon.

    Only useful when used in combination with [`icon`][flet.Tab.icon],
    and [`label`][flet.Tab.label] is not `None`.

    Defaults to `2` pixels of bottom margin.
    If [`Theme.use_material3`][flet.Theme.use_material3] is `False`,
    then defaults to `10` pixels of bottom margin.
    """

    def before_update(self):
        super().before_update()
        assert (self.label is not None) or (self.icon is not None), (
            "Tab must have at least label or icon property set"
        )
