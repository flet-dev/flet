from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["ExpansionPanel", "ExpansionPanelList"]


@control("ExpansionPanel")
class ExpansionPanel(ConstrainedControl, AdaptiveControl):
    """
    A material expansion panel. It can either be expanded or collapsed. Its body is
    only visible when it is expanded.
    """

    header: Optional[Control] = None
    """
    The control to be found in the header of the `ExpansionPanel`. If `can_tap_header`
    is `True`, tapping on the header will expand or collapse the panel.

    If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as
    header.
    """

    content: Optional[Control] = None
    """
    The control to be found in the body of the `ExpansionPanel`. It is displayed below
    the `header` when the panel is expanded.

    If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as
    content.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of the panel.
    """

    expanded: bool = False
    """
    Whether expanded(`True`) or collapsed(`False`). Defaults to `False`.
    """

    can_tap_header: bool = False
    """
    If `True`, tapping on the panel's `header` will expand or collapse it. Defaults to
    `False`.
    """

    splash_color: Optional[ColorValue] = None
    """
    TBD
    """

    highlight_color: Optional[ColorValue] = None
    """
    TBD
    """


@control("ExpansionPanelList")
class ExpansionPanelList(ConstrainedControl):
    """
    A material expansion panel list that lays out its children and animates expansions.
    """

    controls: list[ExpansionPanel] = field(default_factory=list)
    """
    A list of `ExpansionPanel`s to display inside `ExpansionPanelList`.
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider when
    `ExpansionPanel.expanded` is `False`.
    """

    elevation: Number = 2
    """
    Defines the elevation of the children controls (`ExpansionPanel`s), while it is
    expanded. Default value is `2`.
    """

    expanded_header_padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(vertical=16.0)
    )
    """
    Defines the padding around the header when expanded.
    """

    expand_icon_color: Optional[ColorValue] = None
    """
    The color of the icon. Defaults to
    `colors.BLACK_54` in light theme mode and `colors.WHITE_60` in dark theme mode.
    """

    spacing: Optional[Number] = None
    """
    The size of the gap between the `ExpansionPanel`s when expanded.
    """

    on_change: Optional[ControlEventHandler["ExpansionPanelList"]] = None
    """
    Called when an `ExpansionPanel` is expanded or collapsed. The event's data
    (`e.data`), contains the index of the `ExpansionPanel` which triggered this event.
    """

    def before_update(self):
        super().before_update()
        assert self.elevation is None or self.elevation >= 0, (
            "elevation cannot be negative"
        )
