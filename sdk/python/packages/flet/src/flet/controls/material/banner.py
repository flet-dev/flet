from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.dialog_control import DialogControl
from flet.controls.margin import MarginValue
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
)

__all__ = ["Banner"]


@control("Banner")
class Banner(DialogControl):
    """
    A banner displays an important, succinct message, and provides actions for users to
    address (or dismiss the banner). A user action is required for it to be dismissed.

    Banners are displayed at the top of the screen, below a top app bar. They are
    persistent and non-modal, allowing the user to either ignore them or interact with
    them at any time.

    Raises:
        AssertionError: if [`content`][(c).] is not visible.
        AssertionError: if [`elevation`][(c).] is negative.
        AssertionError: if [`actions`][(c).] does not contain at least one visible
            action Control.
    """

    content: StrOrControl
    """
    The content of this banner.

    Typically a [`Text`][flet.Text] control.
    """

    actions: list[Control]
    """
    The set of actions that are displayed at the bottom or trailing side of this banner.

    Typically this is a list of [`TextButton`][flet.TextButton]
    controls.
    """

    leading: Optional[IconDataOrControl] = None
    """
    The leading Control of this banner.

    Typically an [`Icon`][flet.Icon] control.
    """

    leading_padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the [`leading`][flet.Banner.leading] control.

    Defaults to [`BannerTheme.leading_padding`][flet.BannerTheme.leading_padding],
    or if that is `None`, falls back to `Padding.only(end=16)`.
    """

    content_padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the [`content`][flet.Banner.content].

    If the actions are below the content, this defaults to
    `Padding.only(left=16.0, top=24.0, right=16.0, bottom=4.0)`.

    If the actions are trailing the `content`, this defaults to
    `Padding.only(left=16.0, top=2.0)`.
    """

    force_actions_below: bool = False
    """
    An override to force the [`actions`][flet.Banner.actions] to be below the
    [`content`][flet.Banner.content] regardless of how many there are.

    If this is `True`, the `actions` will be placed below the content. If this is
    `False`, the `actions` will be placed on the trailing side of the `content` if
    `actions` length is `1` and below the `content` if greater than `1`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of the surface of this banner.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color of the shadow below this banner.
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider.
    """

    elevation: Optional[Number] = None
    """
    The elevation of this banner.
    """

    margin: Optional[MarginValue] = None
    """
    The amount of space surrounding this banner.
    """

    content_text_style: Optional[TextStyle] = None
    """
    The style to be used for the [`Text`][flet.Text] controls in the
    [`content`][flet.Banner.content].
    """

    min_action_bar_height: Number = 52.0
    """
    The optional minimum action bar height.
    """

    on_visible: Optional[ControlEventHandler["Banner"]] = None
    """
    Called when this banner is shown or made visible for the first time.
    """

    def before_update(self):
        super().before_update()
        assert self.elevation is None or self.elevation >= 0, (
            f"elevation must be greater than or equal to 0, got {self.elevation}"
        )
        if isinstance(self.content, Control):
            assert self.content.visible, "content must be visible"
        assert any(a.visible for a in self.actions), (
            "actions must contain at minimum one visible action Control"
        )
