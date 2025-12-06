from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
)

__all__ = ["NavigationRail", "NavigationRailDestination", "NavigationRailLabelType"]


class NavigationRailLabelType(Enum):
    NONE = "none"
    ALL = "all"
    SELECTED = "selected"


@control("NavigationRailDestination")
class NavigationRailDestination(Control):
    """
    Represents a destination in a `NavigationRail`.
    """

    icon: Optional[IconDataOrControl] = None
    """
    The [name of the icon](https://flet.dev/docs/reference/icons) or `Control` of the
    destination.

    If `selected_icon` is provided, this will only be displayed when the destination is
    not selected.

    To make the NavigationRail more accessible, consider choosing an icon with a stroked
    and filled version, such as `ft.Icons.CLOUD` and `ft.Icons.CLOUD_QUEUE`. The icon
    should be set to the stroked version and `selected_icon` to the filled version.
    """

    selected_icon: Optional[IconDataOrControl] = None
    """
    The [name](https://flet.dev/docs/reference/icons) of alternative icon or `Control`
    displayed when this destination is selected.

    If this icon is not provided, the NavigationRail will display `icon` in either
    state.
    """

    label: Optional[StrOrControl] = None
    """
    A string or Control representing the destination's label.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space to inset the destination item.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the
    [`indicator_shape`][(c).] when
    this destination is selected.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    The shape of the selection indicator.
    """


@control("NavigationRail")
class NavigationRail(LayoutControl):
    """
    A material widget that is meant to be displayed at the left or right of an app to
    navigate between a small number of views, typically between three and five.

    ```python
    ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.STAR, label="Star"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.ADD),label="Add"),
            ft.NavigationRailDestination(icon=ft.Icons.DELETE, label=ft.Text("Delete")
        ],
        height=200,
        width=100,
    )
    ```

    """

    destinations: list[NavigationRailDestination] = field(default_factory=list)
    """
    Defines the appearance of the button items that are arrayed within the navigation
    rail.

    The value must be a list of two or more `NavigationRailDestination` instances.
    """

    elevation: Optional[Number] = None
    """
    Controls the size of the shadow below the NavigationRail.

    Defaults to `0.0`.

    Raises:
        ValueError: If [`elevation`][(c).] is negative.
    """

    selected_index: Optional[int] = None
    """
    The index into `destinations` for the current selected `NavigationRailDestination`
    or `None` if no destination is selected.
    """

    extended: bool = False
    """
    Indicates that the NavigationRail should be in the extended state.

    The extended state has a wider rail container, and the labels are positioned next to
    the icons. `min_extended_width` can be used to set the minimum width of the rail
    when it is in this state.

    The rail will implicitly animate between the extended and normal state.

    If the rail is going to be in the extended state, then the `label_type` must be set
    to `none`.
    """

    label_type: Optional[NavigationRailLabelType] = None
    """
    Defines the layout and behavior of the labels for the default, unextended navigation
    rail.

    When a navigation rail is extended, the labels are always shown.

    Defaults to `None` - no labels are shown.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Sets the color of the Container that holds all of the NavigationRail's contents.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the navigation rail's indicator.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    The shape of the navigation rail's indicator.

    Defaults to `StadiumBorder()`.
    """

    leading: Optional[Control] = None
    """
    An optional leading control in the rail that is placed above the destinations.

    Its location is not affected by `group_alignment`.

    Typically a [`FloatingActionButton`][flet.], but
    may also be a non-button, such as a logo.
    """

    trailing: Optional[Control] = None
    """
    An optional trailing control in the rail that is placed below the destinations.

    Its location is affected by `group_alignment`.

    This is commonly a list of additional options or destinations that is usually only
    rendered when `extended=True`.
    """

    min_width: Optional[Number] = None
    """
    The smallest possible width for the rail regardless of the destination's icon or
    label size.

    Defaults to `72`.

    This value also defines the min width and min height of the destinations.

    To make a compact rail, set this to `56` and use `label_type='none'`.

    Raises:
        ValueError: If [`min_width`][(c).] is negative.
    """

    min_extended_width: Optional[Number] = None
    """
    The final width when the animation is complete for setting `extended` to `True`.

    Defaults to `256`.

    Raises:
        ValueError: If [`min_extended_width`][(c).] is negative.
    """

    group_alignment: Optional[Number] = None
    """
    The vertical alignment for the group of destinations within the rail.

    The NavigationRailDestinations are grouped together with the trailing widget,
    between the leading widget and the bottom of the rail.

    The value must be between `-1.0` and `1.0`.

    If `group_alignment` is `-1.0`, then the items are aligned to the top. If
    `group_alignment` is `0.0`, then the items are aligned to the center. If
    `group_alignment` is `1.0`, then the items are aligned to the bottom.

    Defaults to `-1.0`.
    """

    selected_label_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.] of a
    destination's label when it is selected.

    When a destination is not selected, `unselected_label_text_style` will instead be
    used.
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.] of a
    destination's label when it is not selected.

    When a destination is selected, `selected_label_text_style` will instead be used.
    """

    use_indicator: Optional[bool] = None
    """
    Whether to add a rounded navigation indicator behind the selected destination's icon.

    The indicator's shape will be circular if [`label_type`][(c).]
    is [`NavigationRailLabelType.NONE`][flet.], or a
    [`StadiumBorder`][flet.] if [`label_type`][(c).]
    is [`NavigationRailLabelType.ALL`][flet.] or
    [`NavigationRailLabelType.SELECTED`][flet.].

    If `None`, defaults to
    [`NavigationRailTheme.use_indicator`][flet.].
    If that is also `None`, defaults to [`Theme.use_material3`][flet.].
    """  # noqa: E501

    on_change: Optional[ControlEventHandler["NavigationRail"]] = None
    """
    Called when selected destination changed.
    """

    def before_update(self):
        super().before_update()
        if self.elevation is not None and self.elevation < 0:
            raise ValueError("elevation cannot be negative")
        if self.min_width is not None and self.min_width < 0:
            raise ValueError("min_width cannot be negative")
        if self.min_extended_width is not None and self.min_extended_width < 0:
            raise ValueError("min_extended_width cannot be negative")
