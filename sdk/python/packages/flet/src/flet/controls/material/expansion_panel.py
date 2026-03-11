from dataclasses import dataclass, field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import (
    Event,
    EventHandler,
)
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import Padding, PaddingValue
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["ExpansionPanel", "ExpansionPanelList", "ExpansionPanelListChangeEvent"]


@dataclass
class ExpansionPanelListChangeEvent(Event["ExpansionPanelList"]):
    """
    Payload for [`ExpansionPanelList.on_change`][flet.] event.
    """

    index: int
    """
    The index of the panel in [`ExpansionPanelList.controls`][flet.] that was toggled.

    Invisible panels (i.e. those with [`visible`][flet.Control.] set to `False`)
    are not counted/indexed.
    """

    expanded: bool
    """
    Whether the toggled panel is expanded (`True`) or
    collapsed (`False`) after the event.
    """


@control("ExpansionPanel")
class ExpansionPanel(LayoutControl, AdaptiveControl):
    """
    A material expansion panel. It can either be expanded or collapsed. Its body is \
    only visible when it is expanded.

    Example:
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
    The control to be found in the header of this panel.

    It is always visible, regardless of whether this panel is expanded or collapsed.
    If [`can_tap_header`][(c).] is `True`, tapping on this `header` will expand or
    collapse this panel.

    If this property is `None`, this panel will have a placeholder `Text` as
    header.
    """

    content: Optional[Control] = None
    """
    The control to be found in the body of this panel.

    It is displayed below the [`header`][(c).] when this panel is [`expanded`][(c).].

    If this property is `None`, this panel will have a placeholder `Text` as
    content.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this panel.
    """

    expanded: bool = False
    """
    Whether this panel is in expanded (`True`) or collapsed (`False`) state.
    """

    can_tap_header: bool = False
    """
    Whether tapping on this panel's [`header`][(c).] will expand or collapse it.
    """

    splash_color: Optional[ColorValue] = None
    """
    Defines the splash color of this panel if [`can_tap_header`][(c).] is `True`, \
    or the splash color of the expand/collapse `IconButton` if \
    [`can_tap_header`][(c).] is `False`.

    If [`can_tap_header`][(c).] is `False`, and [`Theme.use_material3`][flet.] is
    `True`, this field will be ignored, as [`IconButton.splash_color`][flet.]
    will be ignored, and you should use [`highlight_color`][(c).] instead.

    If this is `None`, then the icon button will use its default splash color
    [`Theme.splash_color`][flet.], and this panel will use its default splash color
    [`Theme.splash_color`][flet.] (if [`can_tap_header`][(c).] is `True`).
    """

    highlight_color: Optional[ColorValue] = None
    """
    Defines the highlight color of this panel if [`can_tap_header`][(c).] is `True`, \
    or the highlight color of the expand/collapse `IconButton` \
    if [`can_tap_header`][(c).] is `False`.

    If this is `None`, then the icon button will use its default highlight color
    [`Theme.highlight_color`][flet.], and this panel will use its default highlight
    color [`Theme.highlight_color`][flet.] (if [`can_tap_header`][(c).] is `True`).
    """


@control("ExpansionPanelList")
class ExpansionPanelList(LayoutControl, ScrollableControl):
    """
    A material expansion panel list that lays out its children and animates \
    expansions.

    Example:
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
    The color of the divider when [`ExpansionPanel.expanded`][flet.] is `False`.
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

    on_change: Optional[EventHandler[ExpansionPanelListChangeEvent]] = None
    """
    Called when an item of [`controls`][(c).] is expanded or collapsed.
    """

    def before_update(self):
        super().before_update()
        if self.elevation < 0:
            raise ValueError("elevation must be greater than or equal to zero")
