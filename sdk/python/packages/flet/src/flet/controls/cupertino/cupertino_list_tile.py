from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
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

    title: Control
    subtitle: Optional[Control] = None
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    bgcolor: OptionalColorValue = None
    bgcolor_activated: OptionalColorValue = None
    padding: OptionalPaddingValue = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    toggle_inputs: bool = False
    additional_info: Optional[Control] = None
    leading_size: OptionalNumber = None
    leading_to_title: OptionalNumber = None
    notched: bool = False
    on_click: OptionalControlEventCallable = None
