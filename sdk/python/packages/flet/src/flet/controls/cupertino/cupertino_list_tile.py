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

    Can also serve as a cupertino equivalent of the
    Material [`ListTile`][flet.ListTile].

    Raises:
        AssertionError: If [`title`][(c).] is neither a string nor a visible Control.
    """

    title: StrOrControl
    """
    The primary content of this list tile.

    Typically a [`Text`][flet.Text] control.
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the [`title`][flet.CupertinoListTile.title].

    Typically a [`Text`][flet.Text] control.
    """

    leading: Optional[IconDataOrControl] = None
    """
    A control to display before the [`title`][flet.CupertinoListTile.title].
    """

    trailing: Optional[IconDataOrControl] = None
    """
    A control to display after the [`title`][flet.CupertinoListTile.title].

    Typically an [`Icon`][flet.Icon] control.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The list tile's background color.
    """

    bgcolor_activated: Optional[ColorValue] = None
    """
    The list tile's background color
    after the tile was tapped.
    """

    padding: Optional[PaddingValue] = None
    """
    The tile's internal padding. Insets a CupertinoListTile's contents: its
    [`leading`][flet.CupertinoListTile.leading],
    [`title`][flet.CupertinoListTile.title],
    [`subtitle`][flet.CupertinoListTile.subtitle],
    [`additional_info`][flet.CupertinoListTile.additional_info]
    and [`trailing`][flet.CupertinoListTile.trailing] controls.
    """  # noqa: E501

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][flet.CupertinoListTile.on_click] event callback is
    provided, it is fired after that.
    """

    toggle_inputs: bool = False
    """
    Whether clicking on a list tile should toggle the state of togglable controls
    like [`Radio`][flet.Radio], [`Checkbox`][flet.Checkbox]
    or [`Switch`][flet.Switch] inside the tile.
    """

    additional_info: Optional[StrOrControl] = None
    """
    A `Control` to display on the right of the list tile,
    before [`trailing`][flet.CupertinoListTile.trailing].

    Similar to [`subtitle`][flet.CupertinoListTile.subtitle], an
    [`additional_info`][flet.CupertinoListTile.additional_info] is used to
    display additional information.

    Typically a [`Text`][flet.Text] control.
    """

    leading_size: Optional[Number] = None
    """
    Used to constrain the width and height of
    [`leading`][flet.CupertinoListTile.leading] control.

    Defaults to `30.0`, if [`notched=True`][flet.CupertinoListTile.notched],
    else `28.0`.
    """

    leading_to_title: Optional[Number] = None
    """
    The horizontal space between [`leading`][flet.CupertinoListTile.leading]
    and `[`title`][flet.CupertinoListTile.title].

    Defaults to `12.0`, if [`notched=True`][flet.CupertinoListTile.notched],
    else `16.0`.
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
        assert isinstance(self.title, str) or self.title.visible, (
            "title must be a string or a visible Control"
        )
