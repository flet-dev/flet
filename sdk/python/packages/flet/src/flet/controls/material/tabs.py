from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import Duration, DurationValue
from flet.controls.margin import MarginValue
from flet.controls.material.form_field_control import IconValueOrControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MouseCursor,
    Number,
    StrOrControl,
)

__all__ = ["Tab", "Tabs", "TabBar", "TabBarView", "TabAlignment"]


class TabAlignment(Enum):
    """
    Defines how tabs are aligned horizontally in a [`Tabs`][flet.Tabs].
    """

    START = "start"
    """
    If [`Tabs.scrollable`][flet.Tabs.scrollable] is `True`, tabs are aligned #to the 
    start of the [`Tabs`][flet.Tabs]. Otherwise throws an exception.
    """

    START_OFFSET = "startOffset"
    """
    If `Tabs.scrollable` is `True`, tabs are aligned to the start of the
    [`Tabs`][flet.Tabs] with an offset of 52.0 pixels. Otherwise throws an exception.
    """

    FILL = "fill"
    """
    If `Tabs.scrollable` is `False`, tabs are stretched to fill the
    [`Tabs`][flet.Tabs]. Otherwise throws an exception.
    """

    CENTER = "center"
    """
    Tabs are aligned to the center of the [`Tabs`][flet.Tabs].
    """


@control("Tabs")
class Tabs(ConstrainedControl, AdaptiveControl):
    """
    Used for navigating frequently accessed, distinct content
    categories. Tabs allow for navigation between two or more content views and relies
    on text headers to articulate the different sections of content.
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
        and [`TabBarView.controls`][flet.TabBarView.controls].
    """

    initial_index: int = 0
    """
    The initial index of the selected tab.
    
    Can't be changed after the control is mounted (added to the page tree).
    """

    animation_duration: Optional[DurationValue] = field(
        default_factory=lambda: Duration(milliseconds=250),
    )
    """
    The duration of the animations.
    """

    def before_update(self):
        super().before_update()
        assert self.length >= 0, (
            f"length must be greater than or equal to 0, got {self.length}"
        )
        assert self.length == 0 or (0 <= self.initial_index < self.length), (
            f"initial_index must be between 0 and length - 1 ({self.length - 1}) "
            f"inclusive, got {self.initial_index}"
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
    """

    tabs: list[Control]
    """
    A list of controls.

    Typically [`Tab`][flet.Tab]s.
    """

    selected_index: int = 0
    """
    The index of currently selected tab.
    """

    scrollable: bool = True
    """
    Whether this tab bar can be scrolled horizontally.

    If `scrollable` is `True`, then each tab is as wide as needed for its label and
    the entire Tabs controls is scrollable. Otherwise each tab gets an equal share
    of the available space.
    """

    tab_alignment: Optional[TabAlignment] = None
    """
    Specifies the horizontal alignment of the tabs within the Tabs control.

    Defaults to [`TabAlignment.START`][flet.TabAlignment.START], 
    if [`scrollable=True`][flet.Tabs.scrollable], and to
    [`TabAlignment.FILL`][flet.TabAlignment.FILL], 
    if [`scrollable=False`][flet.Tabs.scrollable].
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the indicator(line that
    appears below the selected tab).
    """

    indicator_border_radius: Optional[BorderRadiusValue] = None
    """
    The radius of the indicator's corners.
    """

    indicator_border_side: Optional[BorderSide] = None
    """
    The color and weight of the horizontal
    line drawn below the selected tab.
    """

    indicator_padding: PaddingValue = 0
    """
    Locates the selected tab's underline relative to the tab's boundary.

    The `indicator_tab_size` property can be used to define the tab indicator's bounds
    in terms of its (centered) tab control with `False`, or the entire tab with `True`.
    """

    indicator_tab_size: Optional[bool] = None
    """
    Whether the indicator should take entire tab.
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
    colors in various
    [`ControlState`][flet.ControlState] states.

    The following states are supported: `ControlState.PRESSED`, 
    `ControlState.HOVERED` and
    `ControlState.FOCUSED`.
    """

    divider_height: Optional[Number] = None
    """
    The height of the divider.

    Defaults to `1.0`.
    """

    indicator_thickness: Number = 2.0
    """
    The thickness of the indicator. Value must be greater than zero.
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

    on_change: Optional[ControlEventHandler["TabBar"]] = None
    """
    Called when [`selected_index`][flet.Tabs.selected_index] changes.
    """

    def __contains__(self, item):
        return item in self.tabs


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

    icon: Optional[IconValueOrControl] = None
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
