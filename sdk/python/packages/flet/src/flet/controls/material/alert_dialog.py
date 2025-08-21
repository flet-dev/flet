from dataclasses import field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MainAxisAlignment,
    Number,
    StrOrControl,
)

__all__ = ["AlertDialog"]


@control("AlertDialog")
class AlertDialog(DialogControl):
    """
    Can be used to inform the user about situations that require acknowledgement.

    It has an optional [`title`][(c).] and an optional list of [`actions`][(c).] . The
    `title` is displayed above the [`content`][(c).] and the `actions` are displayed
    below the `content`.

    Raises:
        AssertionError: If none of [`title`][(c).], [`content`][(c).], or
        [`actions`][(c).] are provided, as the dialog would have nothing to display.
    """

    content: Optional[Control] = None
    """
    The content of this dialog is displayed in the center of this dialog in a
    lighter font.

    Typically this is a [`Column`][flet.Column]
    that contains this dialog's [`Text`][flet.Text] message.
    """

    modal: bool = False
    """
    Whether dialog can be dismissed/closed by clicking the area outside of it.
    """

    title: Optional[StrOrControl] = None
    """
    The title of this dialog is displayed in a large font at its top.

    Typically a [`Text`][flet.Text] control.
    """

    actions: list[Control] = field(default_factory=list)
    """
    A set of actions that are displayed at the bottom of this dialog.

    Typically this is a list of [`TextButton`][flet.TextButton]
    controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this dialog's surface.
    """

    elevation: Optional[Number] = None
    """
    Defines the elevation (z-coordinate) at which this dialog should appear.
    """

    icon: Optional[Control] = None
    """
    A control that is displayed at the top of this dialog.

    Typically a [`Icon`][flet.Icon] control.
    """

    title_padding: Optional[PaddingValue] = None
    """
    Padding around the [`title`][flet.AlertDialog.title].

    If there is no title, no padding will be provided. Otherwise, this padding is used.

    Defaults to providing `24` pixels on the top, left, and right of the
    [`title`][flet.AlertDialog.title].
    If the [`content`][flet.AlertDialog.content] is not `None`, then no bottom padding
    is provided (but see [`content_padding`][flet.AlertDialog.content_padding]).
    If it is not set, then an extra `20` pixels of bottom padding is added to separate
    the `title` from the `actions`.
    """

    content_padding: Optional[PaddingValue] = None
    """
    Padding around the [`content`][flet.AlertDialog.content].

    If there is no `content`, no padding will be provided. Otherwise, padding of 20
    pixels is provided above the content to separate the content from the title, and
    padding of 24 pixels is provided on the left, right, and bottom to separate the
    content from the other edges of this dialog.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Padding around the set of [`actions`][flet.AlertDialog.actions] at the bottom of
    this dialog.

    Typically used to provide padding to the button bar between the button bar and the
    edges of this dialog.

    If are no actions, then no padding will be included. The padding around the button
    bar defaults to zero.
    """

    actions_alignment: Optional[MainAxisAlignment] = None
    """
    Defines the horizontal layout of the actions.

    Internally defaults to `MainAxisAlignment.END`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this dialog.

    Defaults to [`DialogTheme.shape`][flet.DialogTheme.shape]. If it is not set,
    it defaults to `RoundedRectangleBorder(radius=4.0)`.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Padding around this dialog itself.

    Defaults to `Padding.symmetric(vertical=40, horizontal=24)` - 40 pixels
    horizontally and 24 pixels vertically outside of this dialog box.
    """

    icon_padding: Optional[PaddingValue] = None
    """
    Padding around the [`icon`][flet.AlertDialog.icon].
    """

    action_button_padding: Optional[PaddingValue] = None
    """
    The padding that surrounds each button in [`actions`][flet.AlertDialog.actions].
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used to paint a drop shadow
    under this dialog, which reflects this dialog's elevation.
    """

    icon_color: Optional[ColorValue] = None
    """
    The color for the Icon in the [`icon`][flet.AlertDialog.icon] of this dialog.

    If `None`, [`DialogTheme.icon_color`][flet.DialogTheme.icon_color] is used.
    If that is null, defaults to color scheme's
    [`ColorScheme.secondary`][flet.ColorScheme.secondary] if
    [`Theme.use_material3`][flet.Theme.use_material3] is `True`, `Colors.BLACK`
    otherwise.
    """

    scrollable: bool = False
    """
    Determines whether the [`title`][flet.AlertDialog.title] and
    [`content`][flet.AlertDialog.content] controls are wrapped in a scrollable.

    This configuration is used when the `title` and `content` are expected to overflow.
    Both `title` and `content` are wrapped in a scroll view, allowing all overflowed
    content to be visible while still showing the button bar.
    """

    actions_overflow_button_spacing: Optional[Number] = None
    """
    The spacing between [`actions`][flet.AlertDialog.actions] when the `OverflowBar`
    switches to a column layout because the actions don't fit horizontally.

    If the controls in `actions` do not fit into a single row, they are arranged into a
    column. This parameter provides additional vertical space between buttons when it
    does overflow.
    """

    alignment: Optional[Alignment] = None
    """
    How to align this dialog.

    If `None`, then [`DialogTheme.alignment`][flet.DialogTheme.alignment] is used.
    If that is also `None`, the default is [`Alignment.CENTER`][flet.Alignment.CENTER].
    """

    content_text_style: Optional[TextStyle] = None
    """
    The style for the text in the [`content`][flet.AlertDialog.content] of this dialog.

    If `None`, [`DialogTheme.content_text_style`][flet.DialogTheme.content_text_style]
    is used.
    If that's is also `None`, defaults to
    [`TextTheme.body_medium`][flet.TextTheme.body_medium] of
    [Theme.text_theme][flet.Theme.text_theme] if
    [`Theme.use_material3`][flet.Theme.use_material3] is `True`,
    [`TextTheme.title_medium`][flet.TextTheme.title_medium] otherwise.
    """

    title_text_style: Optional[TextStyle] = None
    """
    TBD
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Defines how the contents of this dialog are clipped (or not) to the given `shape`.
    """

    semantics_label: Optional[str] = None
    """
    The semantic label of this dialog used by accessibility frameworks to announce
    screen transitions when this dialog is opened and closed.

    In iOS, if this label is not provided, a semantic label will be inferred from the
    `title` if it is not null.
    """

    barrier_color: Optional[ColorValue] = None
    """
    The color of the modal barrier that
    darkens everything below this dialog.

    If `None`, then [`DialogTheme.barrier_color`][flet.DialogTheme.barrier_color]
    is used. If that is also `None`, the default is `Colors.BLACK_54`.
    """

    def before_update(self):
        super().before_update()
        assert self.title or self.content or self.actions, (
            "AlertDialog has nothing to display. Provide at minimum one of the "
            "following: title, content, actions"
        )
