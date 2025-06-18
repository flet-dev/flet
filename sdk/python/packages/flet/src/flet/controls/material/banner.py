from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.dialog_control import DialogControl
from flet.controls.margin import OptionalMarginValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    IconValueOrControl,
    Number,
    OptionalColorValue,
    OptionalNumber,
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

    Online docs: https://flet.dev/docs/controls/banner
    """

    content: StrOrControl
    """
    The content of the Banner.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    actions: list[Control] = field(default_factory=list)
    """
    The set of actions that are displayed at the bottom or trailing side of the Banner.

    Typically this is a list of [`TextButton`](https://flet.dev/docs/controls/textbutton) 
    controls.
    """

    leading: Optional[IconValueOrControl] = None
    """
    The (optional) leading `Control` of the Banner.

    Typically an [`Icon`](https://flet.dev/docs/controls/icon) control.
    """

    leading_padding: OptionalPaddingValue = None
    """
    The amount of space by which to inset the leading control.

    The value is an instance of [`padding.Padding`](https://flet.dev/docs/reference/types/padding) 
    class or a number.

    Defaults to `16` virtual pixels.
    """

    content_padding: OptionalPaddingValue = None
    """
    The amount of space by which to inset the content.

    The value is an instance of [`padding.Padding`](https://flet.dev/docs/reference/types/padding) 
    class or a number.

    If the actions are below the content, this defaults to 
    `padding.only(left=16.0, top=24.0, right=16.0, bottom=4.0)`.

    If the actions are trailing the content, this defaults to 
    `padding.only(left=16.0, top=2.0)`.
    """

    force_actions_below: bool = False
    """
    An override to force the actions to be below the content regardless of how many 
    there are.

    If this is `True`, the actions will be placed below the content. If this is 
    `False`, the actions will be placed on the trailing side of the content if 
    `actions` length is `1` and below the content if greater than `1`.

    Defaults to `False`.
    """

    bgcolor: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the surface of this Banner.
    """

    surface_tint_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used as an overlay on `bgcolor` 
    to indicate elevation.
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the shadow below the banner.
    """

    divider_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the divider.
    """

    elevation: OptionalNumber = None
    """
    The elevation of the banner.
    """

    margin: OptionalMarginValue = None
    """
    The amount of space surrounding the banner.

    The value is an instance of [`Margin`](https://flet.dev/docs/reference/types/margin) 
    class or a number.
    """

    content_text_style: Optional[TextStyle] = None
    """
    The style to be used for the `Text` controls in the `content`.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    min_action_bar_height: Number = 52.0
    """
    The optional minimum action bar height.

    Defaults to `52`.
    """

    on_visible: OptionalControlEventHandler["Banner"] = None
    """
    Fires when the banner is shown or made visible for the first time.
    """

    def before_update(self):
        super().before_update()
        assert self.elevation is None or self.elevation >= 0, (
            "elevation cannot be negative"
        )
        assert self.content.visible, "content must be visible"
        assert any(a.visible for a in self.actions), (
            "actions must contain at minimum one visible action Control"
        )
