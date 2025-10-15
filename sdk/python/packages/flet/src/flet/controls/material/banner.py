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

    ```python
    banner = ft.Banner(
        leading=ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.PRIMARY),
        content=ft.Text("Backup completed successfully."),
        actions=[ft.TextButton("Dismiss")],
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        open=True,
    )
    page.show_dialog(banner)
    ```
    """

    content: StrOrControl
    """
    The content of this banner.

    Typically a [`Text`][flet.] control.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    actions: list[Control]
    """
    The set of actions that are displayed at the bottom or trailing side of this banner.

    Typically this is a list of [`TextButton`][flet.]
    controls.

    Raises:
        ValueError: If [`actions`][(c).] does not contain at least one visible
            action Control.
    """

    leading: Optional[IconDataOrControl] = None
    """
    The leading Control of this banner.

    Typically an [`Icon`][flet.] control.
    """

    leading_padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the [`leading`][(c).] control.

    Defaults to [`BannerTheme.leading_padding`][flet.],
    or if that is `None`, falls back to `Padding.only(end=16)`.
    """

    content_padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the [`content`][(c).].

    If the actions are below the content, this defaults to
    `Padding.only(left=16.0, top=24.0, right=16.0, bottom=4.0)`.

    If the actions are trailing the `content`, this defaults to
    `Padding.only(left=16.0, top=2.0)`.
    """

    force_actions_below: bool = False
    """
    An override to force the [`actions`][(c).] to be below the
    [`content`][(c).] regardless of how many there are.

    If this is `True`, the [`actions`][(c).] will be placed below the content.
    If this is `False`, the [`actions`][(c).] will be placed on the trailing side
    of the [`content`][(c).] if `actions` length is `1` and below the `content`
    if greater than `1`.
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

    Raises:
        ValueError: If [`elevation`][(c).] is negative.
    """

    margin: Optional[MarginValue] = None
    """
    The amount of space surrounding this banner.
    """

    content_text_style: Optional[TextStyle] = None
    """
    The style to be used for the [`Text`][flet.] controls in the [`content`][(c).].
    """

    min_action_bar_height: Number = 52.0
    """
    The minimum action bar height.
    """

    on_visible: Optional[ControlEventHandler["Banner"]] = None
    """
    Called when this banner is shown or made visible for the first time.
    """

    def before_update(self):
        super().before_update()
        if self.elevation is not None and self.elevation < 0:
            raise ValueError(
                f"elevation must be greater than or equal to 0, got {self.elevation}"
            )
        if isinstance(self.content, Control) and not self.content.visible:
            raise ValueError("content must be visible")
        if not any(a.visible for a in self.actions):
            raise ValueError(
                "actions must contain at minimum one visible action Control"
            )
