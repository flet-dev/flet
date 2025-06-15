from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    IconValueOrControl,
    OptionalColorValue,
    OptionalNumber,
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
    TBD
    """

    icon: Optional[IconValueOrControl] = None
    """
    The [name of the icon](https://flet.dev/docs/reference/icons) or `Control` of the
    destination. 

    Example with icon name:
    ```
    icon=ft.Icons.BOOKMARK
    ```
    Example with Control:
    ```
    icon=ft.Icon(ft.Icons.BOOKMARK)
    ```

    If `selected_icon` is provided, this will only be displayed when the destination is
    not selected.

    To make the NavigationRail more accessible, consider choosing an icon with a stroked
    and filled version, such as `ft.Icons.CLOUD` and `ft.Icons.CLOUD_QUEUE`. The icon
    should be set to the stroked version and `selected_icon` to the filled version.
    """

    selected_icon: Optional[IconValueOrControl] = None
    """
    The [name](https://flet.dev/docs/reference/icons) of alternative icon or `Control`
    displayed when this destination is selected. 

    Example with icon name:
    ```
    selected_icon=ft.Icons.BOOKMARK
    ```
    Example with Control:
    ```
    selected_icon=ft.Icon(ft.Icons.BOOKMARK)
    ```

    If this icon is not provided, the NavigationRail will display `icon` in either
    state.
    """

    label: Optional[StrOrControl] = None
    """
    A string or Control representing the destination's label.
    """

    padding: OptionalPaddingValue = None
    """
    The amount of space to inset the destination item.

    Padding is an instance of
    [`Padding`](https://flet.dev/docs/reference/types/padding) class.
    """

    indicator_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the `indicator_shape` when
    this destination is selected.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    The shape of the selection indicator. The value is an instance of
    [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder) class.
    """


@control("NavigationRail")
class NavigationRail(ConstrainedControl):
    """
    A material widget that is meant to be displayed at the left or right of an app to
    navigate between a small number of views, typically between three and five.

    Online docs: https://flet.dev/docs/controls/navigationrail
    """

    destinations: list[NavigationRailDestination] = field(default_factory=list)
    """
    Defines the appearance of the button items that are arrayed within the navigation
    rail.

    The value must be a list of two or more `NavigationRailDestination` instances.
    """

    elevation: OptionalNumber = None
    """
    Controls the size of the shadow below the NavigationRail.

    Defaults to `0.0`.
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

    Defaults to `False`.
    """

    label_type: Optional[NavigationRailLabelType] = None
    """
    Defines the layout and behavior of the labels for the default, unextended navigation
    rail.

    When a navigation rail is extended, the labels are always shown.

    Value is of type
    [`NavigationRailLabelType`](https://flet.dev/docs/reference/types/navigationraillabeltype)
    and defaults to `None` - no labels are shown.
    """

    bgcolor: OptionalColorValue = None
    """
    Sets the [color](https://flet.dev/docs/reference/colors) of the Container that holds
    all of the NavigationRail's contents.
    """

    indicator_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the navigation rail's
    indicator.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    The shape of the navigation rail's indicator.

    Value is of type
    [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder) and
    defaults to `StadiumBorder()`.
    """

    leading: Optional[Control] = None
    """
    An optional leading control in the rail that is placed above the destinations.

    Its location is not affected by `group_alignment`.

    This is commonly a
    [`FloatingActionButton`](https://flet.dev/docs/controls/floatingactionbutton), but
    may also be a non-button, such as a logo.
    """

    trailing: Optional[Control] = None
    """
    An optional trailing control in the rail that is placed below the destinations.

    Its location is affected by `group_alignment`.

    This is commonly a list of additional options or destinations that is usually only
    rendered when `extended=True`.
    """

    min_width: OptionalNumber = None
    """
    The smallest possible width for the rail regardless of the destination's icon or
    label size.

    Defaults to `72`.

    This value also defines the min width and min height of the destinations.

    To make a compact rail, set this to `56` and use `label_type='none'`.
    """

    min_extended_width: OptionalNumber = None
    """
    The final width when the animation is complete for setting `extended` to `True`.

    Defaults to `256`.
    """

    group_alignment: OptionalNumber = None
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
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) of a
    destination's label when it is selected.

    When a destination is not selected, `unselected_label_text_style` will instead be
    used.
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) of a
    destination's label when it is not selected.

    When a destination is selected, `selected_label_text_style` will instead be used.
    """

    on_change: OptionalControlEventHandler["NavigationRail"] = None
    """
    Fires when selected destination changed.
    """

    def before_update(self):
        super().before_update()
        if self.elevation is not None:
            assert self.elevation >= 0, "elevation cannot be negative"
        if self.min_width is not None:
            assert self.min_width >= 0, "min_width cannot be negative"
        if self.min_extended_width is not None:
            assert self.min_extended_width >= 0, "min_extended_width cannot be negative"
