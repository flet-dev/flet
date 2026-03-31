from typing import Annotated, Optional, Union

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
    Url,
)
from flet.utils.validation import V

__all__ = ["CupertinoListTile"]


@control("CupertinoListTile")
class CupertinoListTile(LayoutControl):
    """
    An iOS-style list tile.

    The CupertinoListTile is a Cupertino equivalent of the Material \
    :class:`~flet.ListTile`.

    ```python
    ft.CupertinoListTile(
        title="Notifications",
        subtitle="Enabled",
        width=400,
        leading=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED),
        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
    )
    ```
    """

    title: Annotated[
        StrOrControl,
        V.str_or_visible_control(),
    ]
    """
    The primary content of this list tile.

    Typically a :class:`~flet.Text` control.

    Raises:
        ValueError: If it is neither a string nor a visible `Control`.
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the :attr:`title`.

    Typically a :class:`~flet.Text` control.
    """

    leading: Optional[IconDataOrControl] = None
    """
    A control to display before the :attr:`title`.
    """

    trailing: Optional[IconDataOrControl] = None
    """
    A control to display after the :attr:`title`.

    Typically an :class:`~flet.Icon` control.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this list tile.
    """

    bgcolor_activated: Optional[ColorValue] = None
    """
    The background color of this list tile after it was tapped.
    """

    padding: Optional[PaddingValue] = None
    """
    The tile's internal padding. Insets a CupertinoListTile's contents: its \
    :attr:`leading`, :attr:`title`, :attr:`subtitle`, :attr:`additional_info` and \
    :attr:`trailing` controls.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if :attr:`on_click` event callback is
    provided, it is fired after that.
    """

    toggle_inputs: bool = False
    """
    Whether clicking on this tile should toggle the state of (visible) toggleable \
    controls like :class:`~flet.Radio`, :class:`~flet.Checkbox` or \
    :class:`~flet.Switch` inside it.
    """

    additional_info: Optional[StrOrControl] = None
    """
    A `Control` to display on the right of the list tile, before :attr:`trailing`.

    Similar to :attr:`subtitle`, an :attr:`additional_info`
    is used to display additional information.

    Typically a :class:`~flet.Text` control.
    """

    leading_size: Optional[Number] = None
    """
    Used to constrain the width and height of :attr:`leading` control.

    Defaults to `30.0`, if :attr:`notched` is `True`, else `28.0`.
    """

    leading_to_title: Optional[Number] = None
    """
    The horizontal space between :attr:`leading` and :attr:`title`.

    Defaults to `12.0`, if :attr:`notched` is `True`, else `16.0`.
    """

    notched: bool = False
    """
    Whether this list tile should be created in an "Inset Grouped" form, known from \
    either iOS Notes or Reminders app.
    """

    on_click: Optional[ControlEventHandler["CupertinoListTile"]] = None
    """
    Called when a user clicks/taps the list tile.
    """
