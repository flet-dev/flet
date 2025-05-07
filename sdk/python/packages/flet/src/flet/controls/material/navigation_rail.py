from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    IconValueOrControl,
    OptionalColorValue,
    OptionalControlEventCallable,
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
    elevation: OptionalNumber = None
    selected_index: int = 0
    extended: bool = False
    label_type: Optional[NavigationRailLabelType] = None
    bgcolor: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    indicator_shape: Optional[OutlinedBorder] = None
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    min_width: OptionalNumber = None
    min_extended_width: OptionalNumber = None
    group_alignment: OptionalNumber = None
    selected_label_text_style: Optional[TextStyle] = None
    unselected_label_text_style: Optional[TextStyle] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        if self.elevation is not None:
            assert self.elevation >= 0, "elevation cannot be negative"
        if self.min_width is not None:
            assert self.min_width >= 0, "min_width cannot be negative"
        if self.min_extended_width is not None:
            assert self.min_extended_width >= 0, "min_extended_width cannot be negative"
