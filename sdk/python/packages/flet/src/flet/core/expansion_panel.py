from dataclasses import field
from typing import List, Optional

from flet.core import padding
from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    ColorValue,
    Number,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
)

__all__ = ["ExpansionPanel", "ExpansionPanelList"]


@control("ExpansionPanel")
class ExpansionPanel(ConstrainedControl, AdaptiveControl):
    """
    A material expansion panel. It can either be expanded or collapsed. Its body is only visible when it is expanded.

    -----

    Online docs: https://flet.dev/docs/controls/expansionpanel
    """

    header: Optional[Control] = None
    content: Optional[Control] = None
    bgcolor: Optional[ColorValue] = None
    expanded: bool = False
    can_tap_header: bool = False

    def before_update(self):
        super().before_update()


@control("ExpansionPanelList")
class ExpansionPanelList(ConstrainedControl):
    """
    A material expansion panel list that lays out its children and animates expansions.

    -----

    Online docs: https://flet.dev/docs/controls/expansionpanellist
    """

    controls: List[ExpansionPanel] = field(default_factory=list)
    divider_color: Optional[ColorValue] = None
    elevation: Number = 2
    expanded_header_padding: PaddingValue = field(
        default_factory=lambda: padding.symmetric(vertical=16.0)
    )
    expand_icon_color: Optional[ColorValue] = None
    spacing: OptionalNumber = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
