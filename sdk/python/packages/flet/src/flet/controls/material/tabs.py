from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import OptionalDurationValue
from flet.controls.margin import OptionalMarginValue
from flet.controls.material.form_field_control import IconValueOrControl
from flet.controls.padding import OptionalPaddingValue, PaddingValue
from flet.controls.text_style import OptionalTextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
    TabAlignment,
)

__all__ = ["Tab", "Tabs"]


@control("Tab")
class Tab(AdaptiveControl):
    """
    TBD
    """

    label: Optional[StrOrControl] = None
    """
    String or Control to display as Tab's name.
    """

    content: Optional[Control] = None
    """
    A `Control` to display below the Tab when it is selected.
    """

    icon: Optional[IconValueOrControl] = None
    """
    An icon to display on the left of Tab text.
    """

    height: OptionalNumber = None
    """
    TBD
    """

    icon_margin: OptionalMarginValue = None
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
    The Tabs control is used for navigating frequently accessed, distinct content
    categories. Tabs allow for navigation between two or more content views and relies
    on text headers to articulate the different sections of content.

    Online docs: https://flet.dev/docs/controls/tabs
    """

    tabs: list[Tab] = field(default_factory=list)
    """
    A list of `Tab` controls.
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

    Value is of type [`TabAlignment`](https://flet.dev/docs/reference/types/tabalignment)
    and defaults to `TabAlignment.START`, if `scrollable=True`, and to
    `TabAlignment.FILL`, if `scrollable=False`.
    """

    animation_duration: OptionalDurationValue = None
    """
    Duration of animation in milliseconds of switching between tabs.

    Defaults to `50`.
    """

    divider_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the divider.
    """

    indicator_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the indicator(line that
    appears below the selected tab).
    """

    indicator_border_radius: OptionalBorderRadiusValue = None
    """
    The radius of the indicator's corners.
    """

    indicator_border_side: Optional[BorderSide] = None
    """
    The [color](https://flet.dev/docs/reference/colors) and weight of the horizontal
    line drawn below the selected tab.
    """

    indicator_padding: PaddingValue = 0
    """
    Locates the selected tab's underline relative to the tab's boundary.

    The `indicator_tab_size` property can be used to define the tab indicator's bounds
    in terms of its (centered) tab widget with `False`, or the entire tab with `True`.
    """

    indicator_tab_size: Optional[bool] = None
    """
    `True` for indicator to take entire tab.
    """

    is_secondary: Optional[bool] = None
    """
    Whether to create a secondary/nested tab bar.

    Secondary tabs are used within a content area to further separate related content
    and establish hierarchy.

    Defaults to `False`.
    """

    label_color: bool = False
    """
    The [color](https://flet.dev/docs/reference/colors) of selected tab labels.
    """

    label_padding: OptionalPaddingValue = None
    """
    The padding around the tab label.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding).
    """

    label_text_style: OptionalTextStyle = None
    """
    The text style of the tab labels.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    unselected_label_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of unselected tab labels.
    """

    unselected_label_text_style: OptionalTextStyle = None
    """
    The text style of the unselected tab labels.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Defines the ink response focus, hover, and splash
    [colors](https://flet.dev/docs/reference/colors) in various
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.

    The following `ControlState` values are supported: `PRESSED`, `HOVERED` and
    `FOCUSED`.
    """

    divider_height: OptionalNumber = None
    """
    The height of the divider.

    Defaults to `1.0`.
    """

    indicator_thickness: Number = 2.0
    """
    The thickness of the indicator. Value must be greater than zero.

    Defaults to `2.0`.
    """

    enable_feedback: Optional[str] = None
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

    The value is [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor)
    enum.
    """

    padding: OptionalPaddingValue = None
    """
    The padding around the Tabs control.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding).
    """

    splash_border_radius: OptionalBorderRadiusValue = None
    """
    Defines the clipping radius of splashes that extend outside the bounds of the tab.

    Value is of type [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius).
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior).
    """

    on_click: OptionalControlEventHandler["Tabs"] = None
    """
    Fires when a tab is clicked.
    """

    on_change: OptionalControlEventHandler["Tabs"] = None
    """
    Fires when `selected_index` changes.
    """

    def __contains__(self, item):
        return item in self.tabs
