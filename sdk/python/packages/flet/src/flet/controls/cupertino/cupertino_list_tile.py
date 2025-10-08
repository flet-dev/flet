from typing import Optional, Union

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

__all__ = ["CupertinoListTile"]


@control("CupertinoListTile")
class CupertinoListTile(LayoutControl):
    """
    An iOS-style list tile.

    The CupertinoListTile is a Cupertino equivalent of the Material [`ListTile`][flet.].

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

    title: StrOrControl
    """
    The primary content of this list tile.

    Typically a [`Text`][flet.] control.

    Raises:
        ValueError: If [`title`][(c).] is neither a string nor a visible Control.
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the [`title`][(c).].

    Typically a [`Text`][flet.] control.
    """

    leading: Optional[IconDataOrControl] = None
    """
    A control to display before the [`title`][(c).].
    """

    trailing: Optional[IconDataOrControl] = None
    """
    A control to display after the [`title`][(c).].

    Typically an [`Icon`][flet.] control.
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
    The tile's internal padding. Insets a CupertinoListTile's contents:
    its [`leading`][(c).], [`title`][(c).], [`subtitle`][(c).],
    [`additional_info`][(c).] and [`trailing`][(c).] controls.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][(c).] event callback is
    provided, it is fired after that.
    """

    toggle_inputs: bool = False
    """
    Whether clicking on this tile should toggle the state of (visible) toggleable
    controls like [`Radio`][flet.], [`Checkbox`][flet.] or [`Switch`][flet.] inside it.
    """

    additional_info: Optional[StrOrControl] = None
    """
    A `Control` to display on the right of the list tile, before [`trailing`][(c).].

    Similar to [`subtitle`][(c).], an [`additional_info`][(c).]
    is used to display additional information.

    Typically a [`Text`][flet.] control.
    """

    leading_size: Optional[Number] = None
    """
    Used to constrain the width and height of [`leading`][(c).] control.

    Defaults to `30.0`, if [`notched`][(c).] is `True`, else `28.0`.
    """

    leading_to_title: Optional[Number] = None
    """
    The horizontal space between [`leading`][(c).] and `[`title`][(c).].

    Defaults to `12.0`, if [`notched`][(c).] is `True`, else `16.0`.
    """

    notched: bool = False
    """
    Whether this list tile should be created in an "Inset Grouped" form, known from
    either iOS Notes or Reminders app.
    """

    on_click: Optional[ControlEventHandler["CupertinoListTile"]] = None
    """
    Called when a user clicks/taps the list tile.
    """

    def before_update(self):
        super().before_update()
        if not (isinstance(self.title, str) or self.title.visible):
            raise ValueError("title must be a string or a visible Control")
