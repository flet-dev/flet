from dataclasses import field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import OptionalTextStyle
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    MainAxisAlignment,
    OptionalColorValue,
    OptionalNumber,
    OptionalString,
    StrOrControl,
)

__all__ = ["AlertDialog"]


@control("AlertDialog")
class AlertDialog(DialogControl):
    """
    An alert dialog informs the user about situations that require acknowledgement.
    An alert dialog has an optional title and an optional list of actions. The title
    is displayed above the content and the actions are displayed below the content.

    Online docs: https://flet.dev/docs/controls/alertdialog
    """

    content: Optional[Control] = None
    """
    The (optional) content of the dialog is displayed in the center of the dialog in
    a lighter font. Typically this is a [`Column`](https://flet.dev/docs/controls/column)
    that contains the dialog's [`Text`](https://flet.dev/docs/controls/text) message.

    Value is of type `Control`.
    """

    modal: bool = False
    """
    Whether dialog can be dismissed/closed by clicking the area outside of it.

    Value is of type `bool` and defaults to `False`.
    """

    title: Optional[StrOrControl] = None
    """
    The (optional) title of the dialog is displayed in a large font at the top of the
    dialog.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    actions: list[Control] = field(default_factory=list)
    """
    The (optional) set of actions that are displayed at the bottom of the dialog.

    Typically this is a list of [`TextButton`](https://flet.dev/docs/controls/textbutton)
    controls.
    """

    bgcolor: OptionalColorValue = None
    """
    The background [color](https://flet.dev/docs/reference/colors) of the dialog's 
    surface.
    """

    elevation: OptionalNumber = None
    """
    Defines the elevation (z-coordinate) at which the dialog should appear.

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber).
    """

    icon: Optional[IconValueOrControl] = None
    """
    A control that is displayed at the top of the dialog. Typically a
    [`Icon`](https://flet.dev/docs/controls/icon) control.
    """

    title_padding: OptionalPaddingValue = None
    """
    Padding around the title.

    If there is no title, no padding will be provided. Otherwise, this padding is used.

    Value is of type
    [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).

    Defaults to providing `24` pixels on the top, left, and right of the title.
    If the `content` is not `None`, then no bottom padding is provided (but see
    [`content_padding`](https://flet.dev/docs/controls/alertdialog#content_padding)).
    If it is not set, then an extra `20` pixels of bottom padding is added to separate
    the title from the actions.
    """

    content_padding: OptionalPaddingValue = None
    """
    Padding around the content.

    If there is no content, no padding will be provided. Otherwise, padding of 20 pixels
    is provided above the content to separate the content from the title, and padding of
    24 pixels is provided on the left, right, and bottom to separate the content from
    the other edges of the dialog.

    Value is of type
    [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).
    """

    actions_padding: OptionalPaddingValue = None
    """
    Padding around the set of actions at the bottom of the dialog.

    Typically used to provide padding to the button bar between the button bar and the
    edges of the dialog.

    If are no actions, then no padding will be included. The padding around the button
    bar defaults to zero.

    Value is of type
    [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).
    """

    actions_alignment: Optional[MainAxisAlignment] = None
    """
    Defines the horizontal layout of the actions.

    Value is of type
    [`MainAxisAlignment`](https://flet.dev/docs/reference/types/mainaxisalignment)
    and defaults to `MainAxisAlignment.END`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the dialog.

    Value is of type
    [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder)
    and defaults to `RoundedRectangleBorder(radius=4.0)`.
    """

    inset_padding: OptionalPaddingValue = None
    """
    Padding around the Dialog itself.

    Value is of type
    [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).

    Defaults to `padding.symmetric(vertical=40, horizontal=24)` - 40 pixels horizontally
    and 24 pixels vertically outside of the dialog box.
    """

    icon_padding: OptionalPaddingValue = None
    """
    Padding around the `icon`.

    Value is of type
    [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).
    """

    action_button_padding: OptionalPaddingValue = None
    """
    The padding that surrounds each button in `actions`.

    Value is of type [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).
    """

    surface_tint_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used as a surface tint overlay 
    on the dialog's background color, which reflects the dialog's elevation.
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to paint a drop shadow 
    under the dialog, which reflects the dialog's elevation.
    """

    icon_color: OptionalColorValue = None
    """
    TBD
    """

    scrollable: bool = False
    """
    TBD
    """

    actions_overflow_button_spacing: OptionalNumber = None
    """
    TBD
    """

    alignment: Optional[Alignment] = None
    """
    TBD
    """

    content_text_style: OptionalTextStyle = None
    """
    TBD
    """

    title_text_style: OptionalTextStyle = None
    """
    TBD
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Controls how the contents of the dialog are clipped (or not) to the given `shape`.

    Value is of type
    [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior)
    and defaults to `ClipBehavior.NONE`.
    """

    semantics_label: OptionalString = None
    """
    The semantic label of the dialog used by accessibility frameworks to announce screen
    transitions when the dialog is opened and closed.

    In iOS, if this label is not provided, a semantic label will be inferred from the
    `title` if it is not null.

    Value is of type `str`.
    """

    barrier_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the modal barrier that 
    darkens everything below the dialog.

    If `None`, the
    [`DialogTheme.barrier_color`](https://flet.dev/docs/reference/types/dialogtheme#barrier_color)
    is used. If it is also `None`, then `Colors.BLACK_54` is used.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.title or self.content or self.actions
        ), "AlertDialog has nothing to display. Provide at minimum one of the "
        "following: title, content, actions"
