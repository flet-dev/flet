from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control, value
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.colors import Colors
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler, Event, EventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import Duration, DurationValue
from flet.controls.layout_control import LayoutControl
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
from flet.utils.validation import V

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
    Defines how tabs are aligned horizontally in a :class:`~flet.Tabs`.
    """

    START = "start"
    """
    If :attr:`flet.TabBar.scrollable` is `True`, tabs are aligned to the start of the \
    :class:`~flet.TabBar`.
    """

    START_OFFSET = "startOffset"
    """
    If :attr:`flet.TabBar.scrollable` is `True`, tabs are aligned to the start of the \
    :class:`~flet.TabBar` with an offset of `52.0` pixels.
    """

    FILL = "fill"
    """
    If :attr:`flet.TabBar.scrollable` is `False`, tabs are stretched to fill the \
    :class:`~flet.TabBar`.
    """

    CENTER = "center"
    """
    Tabs are aligned to the center of the :class:`~flet.TabBar`.
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
    The tab indicator's bounds are as wide as the space occupied by the tab in the tab \
    bar: from the right edge of the previous tab to the left edge of the next tab.
    """

    LABEL = "label"
    """
    The tab's bounds are only as wide as the (centered) tab widget itself.

    This value is used to align the tab's label, typically a [Tab]
    widget's text or icon, with the selected tab indicator.
    """


@dataclass
class TabBarHoverEvent(Event["TabBar"]):
    """
    Represents a hover-state change for a tab in a :class:`~flet.TabBar`.

    This event is emitted by :attr:`flet.TabBar.on_hover` when a pointer
    enters or exits a tab item. When moving directly from one tab to another, the
    handler is typically called twice: first with :attr:`hovering` set to `False`
    for the previous tab, then with :attr:`hovering` set to `True` for the next tab.
    """

    hovering: bool
    """
    Whether a pointer has entered (`True`) or exited (`False`) the tab bar at \
    :attr:`index`.
    """

    index: int
    """
    The index of the tab that is being hovered over.
    """


@value
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

    The :attr:`flet.TabBar.indicator_size` property can be used
    to define the tab indicator's bounds in terms of its (centered) tab control with
    :attr:`flet.TabBarIndicatorSize.LABEL`, or the entire tab
    with :attr:`flet.TabBarIndicatorSize.TAB`.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The radius of the indicator's corners.

    If this value is not `None`, a rounded rectangular tab indicator is
    drawn, otherwise rectangular tab indicator is drawn.
    """


@control("Tabs")
class Tabs(LayoutControl, AdaptiveControl):
    """
    Used for navigating frequently accessed, distinct content categories. Tabs allow \
    for navigation between two or more content views and relies on text headers to \
    articulate the different sections of content.
    """

    content: Control
    """
    The content to display.
    """

    length: Annotated[
        int,
        V.ge(0),
    ]
    """
    The total number of tabs.

    Typically greater than one.

    Note:
        Must match the length of both :attr:`flet.TabBar.tabs`
        and :attr:`flet.TabBarView.controls`. Don't forget to update
        it when adding/removing tabs.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    selected_index: int = 0
    """
    The index of the currently selected tab.

    Supports Python-style negative indexing, where `-1` represents the last tab,
    `-2` the second to last, and so on.

    Note:
        - Must be in range `[-length, length - 1]`.
        - Changing the value of this property will internally trigger
            :meth:`move_to` with :attr:`animation_duration` and
            :attr:`flet.AnimationCurve.EASE` animation curve. To specify
            a different animation curve or duration for this particular change,
            use :meth:`move_to` directly.

    Raises:
        IndexError: If it is not in the range `[-length, length - 1]`.
    """

    animation_duration: DurationValue = field(
        default_factory=lambda: Duration(milliseconds=100),
    )
    """
    The duration of tab animations. For example, the animation that occurs when the \
    selected tab changes.
    """

    on_change: Optional[ControlEventHandler["Tabs"]] = None
    """
    Called when :attr:`selected_index` changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the index of the selected tab.
    """

    def before_update(self):
        super().before_update()
        if self.length >= 0 and not (-self.length <= self.selected_index < self.length):
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

        Additionally, it triggers :attr:`on_change` event and updates
        :attr:`selected_index`.

        Note:
            If `index` is negative, it is interpreted as a Python-style negative index
            (e.g., -1 refers to the last tab). If the resolved index is already the
            currently selected tab, the method returns immediately and does nothing.

        Args:
            index: The index of the tab to select. Must be between in range
                `[-length, length - 1]`.
            animation_curve: The curve to apply to the animation.
            animation_duration: The duration of the animation. If `None` (the default),
                :attr:`flet.Tabs.animation_duration` will be used.

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
class TabBarView(LayoutControl, AdaptiveControl):
    """
    A page view with one child per tab.

    Note:
        The length of :attr:`controls` must be the same as the
        :attr:`~flet.Tabs.length` property of the ancestor :class:`~flet.Tabs`.
    """

    controls: list[Control]
    """
    A list of controls, where each control represents the content of a corresponding \
    tab. So, a control at index `i` in this list is displayed when the \
    :class:`~flet.Tab` at index `i` is selected.

    Note:
        The length of this list must be equal to the number of tabs specified in an
        ancestor :class:`~flet.Tabs` control.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    Defines how the :attr:`controls` will be clipped.
    """

    viewport_fraction: Number = 1.0
    """
    The fraction of the viewport that each page should occupy.

    For example, `1.0` (the default), means each page fills
    the viewport in the scrolling direction.
    """


@control("TabBar")
class TabBar(LayoutControl, AdaptiveControl):
    """
    Used for navigating frequently accessed, distinct content categories. Tabs allow \
    for navigation between two or more content views and relies on text headers to \
    articulate the different sections of content.
    """

    tabs: list[Control]
    """
    A list of controls.

    Typically :class:`~flet.Tab`s.
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
    :attr:`flet.TabBarTheme.tab_alignment` is used.
    If :attr:`flet.TabBarTheme.tab_alignment` is `None` and
    :attr:`flet.Theme.use_material3` is `True`,
    then :attr:`flet.TabAlignment.START_OFFSET` is used if
    :attr:`scrollable` is `True`,
    otherwise :attr:`flet.TabAlignment.FILL` is used.

    If :attr:`flet.TabBarTheme.tab_alignment` is `None`
    and :attr:`flet.Theme.use_material3` is `False`,
    then :attr:`flet.TabAlignment.CENTER` is used if
    :attr:`scrollable` is `True`,
    otherwise :attr:`flet.TabAlignment.FILL` is used.

    Note:
        - If :attr:`scrollable` is `False`, then :attr:`tab_alignment` must be
            either :attr:`flet.TabAlignment.FILL` or :attr:`flet.TabAlignment.CENTER`.
        - If :attr:`scrollable` is `True`, then :attr:`tab_alignment` must be
            :attr:`flet.TabAlignment.START`, :attr:`flet.TabAlignment.START_OFFSET`
            or :attr:`flet.TabAlignment.CENTER`.

    Raises:
        ValueError: If it is not valid for the current
            :attr:`scrollable` configuration.
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the indicator(line that appears below the selected tab).

    Note:
        Will be ignored if :attr:`indicator` or
        :attr:`flet.TabBarTheme.indicator` is not `None`.
    """

    indicator: Optional[UnderlineTabIndicator] = None
    """
    Defines the appearance of the selected tab indicator.

    If this or :attr:`flet.TabBarTheme.indicator` is not `None`,
    :attr:`indicator_color` and
    :attr:`indicator_thickness` properties are ignored.

    The indicator's size is based on the tab's bounds. If
    :attr:`indicator_size`
    is :attr:`flet.TabBarIndicatorSize.TAB`,
    the tab's bounds are as wide as the space occupied by the tab in the tab bar.
    If :attr:`indicator_size` is
    :attr:`flet.TabBarIndicatorSize.LABEL`,
    then the tab's bounds are only as wide as the tab control itself.
    """

    indicator_size: Optional[TabBarIndicatorSize] = None
    """
    Defines how the selected tab indicator's size is computed.

    The size of the selected tab indicator is defined relative to the
    tab's overall bounds if `indicator_size` is
    :attr:`flet.TabBarIndicatorSize.TAB`
    (the default) or relative to the bounds of the tab's control if
    `indicator_size` is :attr:`flet.TabBarIndicatorSize.LABEL`.

    The selected tab's location appearance can be refined further with
    the :attr:`indicator_color`,
    :attr:`indicator_thickness`,
    and :attr:`indicator` properties.
    """

    indicator_animation: Optional[TabIndicatorAnimation] = None
    """
    Specifies the animation behavior of the tab indicator.

    If this is `None`, then the value of
    :attr:`flet.TabBarTheme.indicator_animation` is used.
    If that is also `None`, then the tab indicator will animate linearly if the
    :attr:`indicator_size` is
    :attr:`flet.TabBarIndicatorSize.TAB`, otherwise it will animate
    with an elastic effect if the :attr:`indicator_size` is
    :attr:`flet.TabBarIndicatorSize.LABEL`.
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
    Defines the ink response focus, hover, and splash colors in various \
    :class:`~flet.ControlState` states.

    The following states are supported: `ControlState.PRESSED`,
    `ControlState.HOVERED` and
    `ControlState.FOCUSED`.
    """

    divider_height: Optional[Number] = None
    """
    The height of the divider.

    If `None`, defaults to
    :attr:`flet.TabBarTheme.divider_height`. If this is also
    `None`, `1.0` will be used.
    """

    indicator_thickness: Number = 2.0
    """
    The thickness of the indicator. Value must be greater than zero.

    Note:
        Will be ignored if :attr:`indicator` or
        :attr:`flet.TabBarTheme.indicator` is not `None`.

    Raises:
        ValueError: If :attr:`indicator` is `None` and
            :attr:`indicator_thickness` is not strictly greater than `0`.
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
    The cursor to be displayed when a mouse pointer enters or is hovering over this \
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

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the index of the clicked tab.
    """

    on_hover: Optional[EventHandler[TabBarHoverEvent]] = None
    """
    Called when a tab's (from :attr:`tabs`) hover state in the tab bar changes.

    When hover is moved from one tab directly to another, this will be called
    twice. First to represent hover exiting the initial tab, and then second
    for the pointer entering hover over the next tab.
    """

    def __contains__(self, item):
        return item in self.tabs

    def before_update(self):
        super().before_update()
        if self.indicator is None and self.indicator_thickness <= 0.0:
            raise ValueError(
                f"indicator_thickness must be strictly greater than zero if indicator "
                f"is None, got {self.indicator_thickness}"
            )
        valid_alignments = (
            [TabAlignment.CENTER, TabAlignment.FILL]
            if not self.scrollable
            else [TabAlignment.START, TabAlignment.START_OFFSET, TabAlignment.CENTER]
        )

        if (
            self.tab_alignment is not None
            and self.tab_alignment not in valid_alignments
        ):
            raise ValueError(
                f"If scrollable is {self.scrollable}, tab_alignment must be one of: "
                f"{', '.join(f'TabAlignment.{a.name}' for a in valid_alignments)}."
            )


@control("Tab")
class Tab(AdaptiveControl):
    """
    A Material Design :class:`~flet.TabBar` tab.
    """

    label: Optional[StrOrControl] = None
    """
    The tab's name. Can be either a string or a control.

    Raises:
        ValueError: If both :attr:`label` and :attr:`icon` are not set.
    """

    icon: Optional[IconDataOrControl] = None
    """
    An icon to display on the left of Tab text.
    """

    height: Optional[Number] = None
    """
    The height of the tab.

    If `None`, it will be calculated based on the content of the Tab. When
    :attr:`icon` is not `None` along with :attr:`label`,
    the default `height` is `72.0` pixels. Without an `icon`,
    the `height` is 46.0 pixels.

    Currently, the provided tab height cannot be lower than the default height.
    """

    icon_margin: Optional[MarginValue] = None
    """
    The margin added around the tab's icon.

    Only useful when used in combination with :attr:`icon`,
    and :attr:`label` is not `None`.

    Defaults to `2` pixels of bottom margin.
    If :attr:`flet.Theme.use_material3` is `False`,
    then defaults to `10` pixels of bottom margin.
    """

    def before_update(self):
        super().before_update()
        if not ((self.label is not None) or (self.icon is not None)):
            raise ValueError("Tab must have at least label or icon property set")
