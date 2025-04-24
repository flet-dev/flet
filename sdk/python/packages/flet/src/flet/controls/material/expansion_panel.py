from dataclasses import field
from typing import List, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["ExpansionPanel", "ExpansionPanelList"]


@control("ExpansionPanel")
class ExpansionPanel(ConstrainedControl, AdaptiveControl):
    """
    A material expansion panel. It can either be expanded or collapsed. Its body is only visible when it is expanded.

    Online docs: https://flet.dev/docs/controls/expansionpanel
    """

    header: Optional[Control] = None
    """
    The control to be found in the header of the `ExpansionPanel`. If `can_tap_header` is `True`, tapping on the header will expand or collapse the panel.

    If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as header.
    """

    content: Optional[Control] = None
    """
    The control to be found in the body of the `ExpansionPanel`. It is displayed below the `header` when the panel is expanded.

    If this property is `None`, the `ExpansionPanel` will have a placeholder `Text` as content.
    """

    bgcolor: OptionalColorValue = None
    """
    The background [color](https://flet.dev/docs/reference/colors) of the panel.
    """

    expanded: bool = False
    """
    Whether expanded(`True`) or collapsed(`False`). Defaults to `False`.
    """

    can_tap_header: bool = False
    """
    If `True`, tapping on the panel's `header` will expand or collapse it. Defaults to `False`.
    """

    splash_color: OptionalColorValue = None
    """
    TBD
    """

    highlight_color: OptionalColorValue = None
    """
    TBD
    """


@control("ExpansionPanelList")
class ExpansionPanelList(ConstrainedControl):
    """
    A material expansion panel list that lays out its children and animates expansions.

    Online docs: https://flet.dev/docs/controls/expansionpanellist
    """

    controls: List[ExpansionPanel] = field(default_factory=list)
    divider_color: OptionalColorValue = None
    elevation: Number = 2
    expanded_header_padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(vertical=16.0)
    )
    expand_icon_color: OptionalColorValue = None
    spacing: OptionalNumber = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
