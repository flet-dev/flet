from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import DurationValue, Duration
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
    TabAlignment,
)

__all__ = ["Tab", "Tabs"]


@control("Tab")
class Tab(AdaptiveControl):
    """
    Raises:
        AssertionError: If both [`label`][(c).] and [`icon`][(c).] are not set.
    """

    label: Optional[StrOrControl] = None
    """
    The tab's name. Can be either a string or a control.
    """

    content: Optional[Control] = None
    """
    The tab's content to display when it is selected.
    """

    icon: Optional[IconValueOrControl] = None
    """
    An icon to display on the left of Tab text.
    """

    height: Optional[Number] = None
    """
    TBD
    """

    icon_margin: Optional[MarginValue] = None
    """
    TBD
    """

    def before_update(self):
        super().before_update()
        assert (self.label is not None) or (self.icon is not None), (
            "Tab must have at least label or icon property set"
        )


@control("Tabs")
class Tabs(ConstrainedControl, AdaptiveControl):
    """
    Used for navigating frequently accessed, distinct content
    categories. Tabs allow for navigation between two or more content views and relies
    on text headers to articulate the different sections of content.
    """

    tabs: list[Tab] = field(default_factory=list)
    """
    A list of [`Tab`][flet.Tab] controls.
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
    [`TabAlignment.FILL`][flet.TabAlignment.FILL], if [`scrollable=False`][flet.Tabs.scrollable].
    """

    animation_duration: DurationValue = field(default_factory=lambda: Duration(milliseconds=50))
    """
    Duration of animation in milliseconds of switching between tabs.
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

    The following states are supported: `ControlState.PRESSED`, `ControlState.HOVERED` and
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

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The content will be clipped (or not) according to this option.
    """

    on_click: Optional[ControlEventHandler["Tabs"]] = None
    """
    Called when a tab is clicked.
    """

    on_change: Optional[ControlEventHandler["Tabs"]] = None
    """
    Called when [`selected_index`][flet.Tabs.selected_index] changes.
    """

    def __contains__(self, item):
        return item in self.tabs
