from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["ExpansionPanel", "ExpansionPanelList"]


@control("ExpansionPanel")
class ExpansionPanel(LayoutControl, AdaptiveControl):
    """
    A material expansion panel. It can either be expanded or collapsed. Its body is
    only visible when it is expanded.

    ```python
    ft.ExpansionPanelList(
        width=400,
        controls=[
            ft.ExpansionPanel(
                header=ft.Text("Shipping address"),
                content=ft.Text("123 Market Street, Springfield"),
                expanded=True,
            ),
            ft.ExpansionPanel(
                header=ft.Text("Billing address"),
                content=ft.Text("Same as shipping"),
            ),
        ],
    )
    ```
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
    Whether expanded(`True`) or collapsed(`False`).
    """

    can_tap_header: bool = False
    """
    If `True`, tapping on the panel's `header` will expand or collapse it.
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
class ExpansionPanelList(LayoutControl):
    """
    A material expansion panel list that lays out its children and animates expansions.

    ```python
    ft.ExpansionPanelList(
        width=400,
        controls=[
            ft.ExpansionPanel(
                header=ft.Text("Details"),
                content=ft.Text("More information here"),
                expanded=True,
            ),
            ft.ExpansionPanel(
                header=ft.Text("History"),
                content=ft.Text("View previous updates"),
            ),
        ],
    )
    ```
    """

    controls: list[ExpansionPanel] = field(default_factory=list)
    """
    A list of panels to display.
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider when
    [`ExpansionPanel.expanded`][flet.] is `False`.
    """

    elevation: Number = 2
    """
    Defines the elevation of the [`controls`][(c).], when expanded.

    Raises:
        ValueError: If it is less than zero.
    """

    expanded_header_padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(vertical=16.0)
    )
    """
    Defines the padding around the header when expanded.
    """

    expand_icon_color: Optional[ColorValue] = None
    """
    The color of the icon.

    Defaults to [`Colors.BLACK_54`][flet.] in light theme mode and
    [`Colors.WHITE_60`][flet.] in dark theme mode.
    """

    spacing: Optional[Number] = None
    """
    The size of the gap between the [`controls`][(c).]s when expanded.
    """

    on_change: Optional[ControlEventHandler["ExpansionPanelList"]] = None
    """
    Called when an item of [`controls`][(c).] is expanded or collapsed.

    The [`data`][flet.Event.] property of the event handler argument contains the
    index of the child panel (in [`controls`][(c).]) which triggered this event.
    """

    def before_update(self):
        super().before_update()
        if self.elevation < 0:
            raise ValueError("elevation must be greater than or equal to zero")
