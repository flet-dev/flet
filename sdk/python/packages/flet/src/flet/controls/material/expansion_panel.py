from dataclasses import dataclass, field
from typing import Annotated, Optional

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
from flet.utils.validation import V

__all__ = ["ExpansionPanel", "ExpansionPanelList", "ExpansionPanelListChangeEvent"]


@dataclass
class ExpansionPanelListChangeEvent(Event["ExpansionPanelList"]):
    """
    Payload for :attr:`flet.ExpansionPanelList.on_change` event.
    """

    index: int
    """
    The index of the panel in :attr:`flet.ExpansionPanelList.controls` that was toggled.

    Panels with :attr:`~flet.Control.visible` set to `False` are not counted/indexed.
    This means the value may differ from the panel's position in the original
    :attr:`flet.ExpansionPanelList.controls` list when some panels are invisible.
    To map it back, filter :attr:`flet.ExpansionPanelList.controls` to only visible
    panels and use this index on that filtered list.
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
    If :attr:`can_tap_header` is `True`, tapping on this `header` will expand or
    collapse this panel.

    If this property is `None`, this panel will have a placeholder `Text` as
    header.
    """

    content: Optional[Control] = None
    """
    The control to be found in the body of this panel.

    It is displayed below the :attr:`header` when this panel is :attr:`expanded`.

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
    Whether tapping on this panel's :attr:`header` will expand or collapse it.
    """

    splash_color: Optional[ColorValue] = None
    """
    Defines the splash color of this panel if :attr:`can_tap_header` is `True`, or the \
    splash color of the expand/collapse `IconButton` if :attr:`can_tap_header` is \
    `False`.

    If :attr:`can_tap_header` is `False`, and :attr:`flet.Theme.use_material3` is
    `True`, this field will be ignored, as :attr:`flet.IconButton.splash_color`
    will be ignored, and you should use :attr:`highlight_color` instead.

    If this is `None`, then the icon button will use its default splash color
    :attr:`flet.Theme.splash_color`, and this panel will use its default splash color
    :attr:`flet.Theme.splash_color` (if :attr:`can_tap_header` is `True`).
    """

    highlight_color: Optional[ColorValue] = None
    """
    Defines the highlight color of this panel if :attr:`can_tap_header` is `True`, or \
    the highlight color of the expand/collapse `IconButton` if :attr:`can_tap_header` \
    is `False`.

    If this is `None`, then the icon button will use its default highlight color
    :attr:`flet.Theme.highlight_color`, and this panel will use its default highlight
    color :attr:`flet.Theme.highlight_color` (if :attr:`can_tap_header` is `True`).
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
    The color of the divider when :attr:`flet.ExpansionPanel.expanded` is `False`.
    """

    elevation: Annotated[
        Number,
        V.ge(0),
    ] = 2
    """
    Defines the elevation of the :attr:`controls`, when expanded.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
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

    Defaults to :attr:`flet.Colors.BLACK_54` in light theme mode and
    :attr:`flet.Colors.WHITE_60` in dark theme mode.
    """

    spacing: Optional[Number] = None
    """
    The size of the gap between the :attr:`controls`s when expanded.
    """

    on_change: Optional[EventHandler[ExpansionPanelListChangeEvent]] = None
    """
    Called when an item of :attr:`controls` is expanded or collapsed.
    """
