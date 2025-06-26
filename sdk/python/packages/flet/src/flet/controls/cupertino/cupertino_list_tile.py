from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    IconValueOrControl,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
    UrlTarget,
)

__all__ = ["CupertinoListTile"]


@control("CupertinoListTile")
class CupertinoListTile(ConstrainedControl):
    """
    An iOS-style list tile. The CupertinoListTile is a Cupertino equivalent of Material
    ListTile.

    Online docs: https://flet.dev/docs/controls/cupertinolisttile
    """

    title: StrOrControl
    """
    A `Control` to display as primary content of the list tile.
    
    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the title.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    leading: Optional[IconValueOrControl] = None
    """
    A `Control` to display before the `title`.
    """

    trailing: Optional[IconValueOrControl] = None
    """
    A `Control` to display after the title.
    
    Typically an [`Icon`](https://flet.dev/docs/controls/icon) control.
    """

    bgcolor: OptionalColorValue = None
    """
    The list tile's background [color](https://flet.dev/docs/reference/colors).
    """

    bgcolor_activated: OptionalColorValue = None
    """
    The list tile's background [color](https://flet.dev/docs/reference/colors)
    after the tile was tapped.
    """

    padding: OptionalPaddingValue = None
    """
    The tile's internal padding. Insets a CupertinoListTile's contents: its 
    `leading`, `title`, `subtitle`, `additional_info` and `trailing` controls.

    Padding is an instance of 
    [`Padding`](https://flet.dev/docs/reference/types/padding) class.
    """

    url: Optional[str] = None
    """
    The URL to open when the list tile is clicked. If registered, `on_click`
    event is fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget)
    and defaults to `UrlTarget.BLANK`.
    """

    toggle_inputs: bool = False
    """
    Whether clicking on a list tile should toggle the state of `Radio`, `Checkbox`
    or `Switch` inside the tile. Default is `False`.
    """

    additional_info: Optional[StrOrControl] = None
    """
    A `Control` to display on the right of the list tile, before `trailing`.
    
    Similar to `subtitle`, an `additional_info` is used to display additional 
    information. Usually a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    leading_size: OptionalNumber = None
    """
    Used to constrain the width and height of `leading` control.
    
    Defaults to `30.0`, if `notched=True`, else `28.0`.
    """

    leading_to_title: OptionalNumber = None
    """
    The horizontal space between `leading` and `title`.
    
    Defaults to `12.0`, if `notched=True`, else `16.0`.
    """

    notched: bool = False
    """
    If `True`, list tile will be created in an "Inset Grouped" form, known from
    either iOS Notes or Reminders app.

    Defaults to `False`.
    """

    on_click: OptionalControlEventHandler["CupertinoListTile"] = None
    """
    Fires when a user clicks or taps the list tile.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.title, str) or self.title.visible, (
            "title must be a string or a visible Control"
        )
